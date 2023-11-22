from bardapi import Bard

class BardAPI:

    def __init__(self, token):
        self.bard = Bard(token = token, timeout = 30)

    def summarize(self, prompt):
        template = f"""
        Summarize the email by highlighting most important information. Do not use any information outside the email to generate the summary. Do not add any filler content like "Sure, here is the summary".

        Here is the email: {prompt}
        """
        response = self.bard.get_answer(template)
        bard_response = response['content']
        return bard_response
        
