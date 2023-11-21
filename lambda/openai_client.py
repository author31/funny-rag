import os
import together
from tqdm import tqdm
from typing import List
from openai import OpenAI
from cluster import Cluster
from dotenv import load_dotenv

load_dotenv()

class OpenAIClient(Cluster):
    def __init__(self) -> None:
        super().__init__()
        self.client= OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_name= "gpt-3.5-turbo-1106"
        
    def post_processing(self) -> None:
        unique_cluster_idxes = self.get_unqiue_cluster_idx()
        for cluster_idx in tqdm(unique_cluster_idxes, desc="Generating titles"):
            clustered_result = self.get_records_by_cluster_idx(cluster_idx)
            generated_title = self.generate_title(clustered_result)
            self.insert_to_cluster_title_table([cluster_idx, generated_title])
        
    @property
    def kw_extract_prompt_template(self) -> str:
        return \
        """
        I have read the following texts:
        {texts}
        Based on these texts, what is an interesting and thought-provoking question that arises from the key themes or ideas presented?
        """
    
    @property
    def title_generate_prompt_template(self) -> str:
        return \
        """
        Using the following list of keywords, create a compelling and coherent title. The title should integrate these keywords in a way that forms a clear and engaging topic or theme.
        keywords: {keywords}
        """

    def process(self) -> None:
        self.pre_processing()
        unique_cluster_idxes = self.get_unqiue_cluster_idx()
        for cluster_idx in tqdm(unique_cluster_idxes, desc="Generating titles"):
            clustered_result = self.get_records_by_cluster_idx(cluster_idx)
            kw_prompt = self.apply_extract_kw_prompt_template(clustered_result, prompt_template=self.kw_extract_prompt_template)
            keywords = self._call_api(prompt= kw_prompt)
            title_prompt = self.apply_generate_title_prompt_template(keywords, prompt_template=self.title_generate_prompt_template)
            generated_title = self._call_api(prompt= title_prompt)
            self.insert_to_cluster_title_table([cluster_idx, generated_title])
        
    
    def apply_extract_kw_prompt_template(self, clusterd_data: List[str], prompt_template: str=None) -> str:
        texts = "\n".join(f"Text {i+1}: {text}" for i, text in enumerate(clusterd_data))
        return prompt_template.format(texts=texts)
    
    def apply_generate_title_prompt_template(self, keywords: str, prompt_template: str=None) -> str:
        keywords = "\n".join(f"Keyword {i+1}: {keyword}" for i, keyword in enumerate(keywords))
        return prompt_template.format(keywords=keywords)

    def extract_keywords(self, clustered_data: List) -> None:
        prompt = "I have read the following texts:\n\n"
        prompt += "\n\n".join(f"Text {i+1}: {text}" for i, text in enumerate(clustered_data))
        prompt += "\n\nBased on these texts, what is an interesting and thought-provoking question that arises from the key themes or ideas presented?"
        return self._call_api(prompt)
    
    def generate_title(self, clustered_data: List) -> None:
        keywords = self.extract_keywords(clustered_data)
        prompt = "Using the following list of keywords, create a compelling and coherent title. The title should integrate these keywords in a way that forms a clear and engaging topic or theme."
        prompt += "keywords: " + keywords
        return self._call_api(prompt)

    def _call_api(self, prompt: str) -> str:
        if not prompt: return
        response = self.client.chat.completions.create(
            model= self.model_name,
            messages = [
                {"role": "system", "content": "You are an assistant"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content