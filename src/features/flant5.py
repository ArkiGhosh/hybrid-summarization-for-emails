from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class FlanT5:

    def __init__(self):
        self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")

    def summarize(self, prompt):
        template = f"""
        Summarize the email by highlighting most important information 

        {prompt}

        Summary:
        """
        inputs = self.tokenizer(template, return_tensors="pt")
        outputs = self.tokenizer.decode(self.model.generate(**inputs, min_length = 25, max_length = 100)[0], skip_special_tokens=True)
        return outputs
        
