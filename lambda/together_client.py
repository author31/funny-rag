import os
import together
from tqdm import tqdm
from typing import List
from cluster import Cluster
from dotenv import load_dotenv

load_dotenv()
together.api_key = os.getenv("TOGETHER_API_KEY")

class TogetherClient(Cluster):
    def __init__(self) -> None:
        super().__init__()
        self.model_name = "mistralai/Mistral-7B-Instruct-v0.1"
        self.max_tokens = 512
        self.temperature = 0.7
        self.top_p = 5
        self.top_k = 60
        
    @property
    def prompt_template(self):
        return \
        """
        <s>[INST] I have read the following texts: \n 
        {texts}
        \n Based on these given texts, what is an interesting and thought-provoking question that arises from the
        key themes or ideas presented, be noted that the length of the question shouldnt be longer than 255 chars, 
        output only one question without additional commentary or analysis </s>[INST]
        """

    def process(self) -> None:
        self.pre_processing()
        unique_cluster_idxes = self.get_unqiue_cluster_idx()
        for cluster_idx in tqdm(unique_cluster_idxes, desc="Generating titles"):
            clustered_result = self.get_records_by_cluster_idx(cluster_idx)
            titles = [c["title"] for c in clustered_result]
            prompt = self.apply_template(titles, prompt_template=self.prompt_template)
            generated_title = self._call_api(prompt= prompt)
            self.insert_to_cluster_title_table([cluster_idx, generated_title.strip()])

    def apply_template(self, clusterd_data: List[str], prompt_template: str = None):
        prompt_template = prompt_template
        texts = "\n".join(f"Text {i+1}: {text}" for i, text in enumerate(clusterd_data))
        return prompt_template.format(texts=texts)
        
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