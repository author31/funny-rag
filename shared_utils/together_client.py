import os
import re
import together
from tqdm import tqdm
from typing import List
from .cluster import Cluster
from dotenv import load_dotenv

load_dotenv()
together.api_key = os.getenv("TOGETHER_API_KEY")

class TogetherClient(Cluster):
    def __init__(self) -> None:
        super().__init__()
        self.model_name = "mistralai/Mistral-7B-Instruct-v0.1"
        self.max_tokens = 512
        self.temperature = 0.7
        self.top_p = 0.7
        self.top_k = 70
        
    @property
    def prompt_template(self):
        return \
        """
        <s>[INST] I have read the following texts: \n 
        {texts}
        \n Based on these given texts, what is an interesting and thought-provoking question that arises from the
        key themes or ideas presented, the length of the question must be less than 255 chars, 
        output only one question without additional commentary or analysis </s>[INST]
        """
    
    @property
    def finalized_prompt_template(self):
        return \
        """
        <s>[INST] Based on the following texts, generate a single thought-provoking question arising from given texts. 
        The question should be less than 255 characters and should be presented without any additional commentary or analysis. 
        Texts: 
        {texts}

        Output: A single, concise question. 
        </s>[INST]
        """
        
    @property
    def retrieve_prompt_template(self):
        return \
        """
        <s>[INST] Read through the provided texts, which are the titles from the website named Hacker News: {texts}
        to answer the following question: {question}
        Consider the depth of analysis, context, and relavance to the topic when evaluating the response</s>[INST]
        """

    def process(self) -> None:
        self.pre_processing()
        unique_cluster_idxes = self.get_unqiue_cluster_idx()
        for cluster_idx in tqdm(unique_cluster_idxes, desc="Generating titles"):
            clustered_result = self.get_records_by_cluster_idx(cluster_idx)
            titles = [c["title"] for c in clustered_result]
            prompt = self.apply_template(titles, prompt_template=self.finalized_prompt_template)
            generated_title = self._call_api(prompt= prompt)
            santitized_title = self._santitize_word(generated_title)
            self.insert_to_cluster_title_table([cluster_idx, santitized_title])

    def retrieve_answer(self, question: str, titles: List):
        assert titles, "Contexts have to be provided"
        prompt = self.retrieve_prompt_template.format(question=question, texts=titles)
        return self._call_api(prompt=prompt)
        
    def apply_template(self, clusterd_data: List[str], prompt_template: str = None):
        prompt_template = prompt_template
        texts = "\n".join(f"Text {i+1}: {text}" for i, text in enumerate(clusterd_data))
        return prompt_template.format(texts=texts)
        
    def _santitize_word(self, word: str) -> str:
        word = word.split("?")[0].strip() + "?"
        word = word.replace('"', "")
        return re.sub("^\d+\.\s", "", word.lower())

    def _call_api(self, prompt=None):
        if not prompt: return
        result = together.Complete.create(
            prompt=prompt,
            model=self.model_name,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            top_k=self.top_k
        )
        return result["output"]["choices"][0]["text"]