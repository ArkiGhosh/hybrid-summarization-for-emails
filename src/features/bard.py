from bardapi import Bard

class BardAPI:

    def __init__(self, token):
        self.bard = Bard(token = token, timeout = 30)

    def summarize(self, prompt):
        template = f"""
        Summarize the email by highlighting most important information 

        {prompt}

        Summary:
        """
        response = self.bard.get_answer(template)
        bard_response = response['content']
        return bard_response
        
