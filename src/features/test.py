from preprocess import sanitize, remove_duplicates

text = """
Subject: Happy New Year 2023!

~~~~~~~~~~~~~~~~~~~~~~~

Happy New Year, everyone! I hope you all had a wonderful holiday season and are looking forward to a happy and prosperous 2023.

%^&()!@#%^&()!@

This year, I am especially grateful for all of the amazing people in my life. You make me a better person and I am so lucky to have you in my corner.

~@#%^&()~@#%^&()

I wish you all the best in the new year. May it be filled with good health, happiness, and success.

Cheers!

~~~~~~~~~~~~~~~~~~~~~~~

This is a string with some 𝒖𝒏𝒊𝒄𝒐𝒅𝒆 characters.

"""

sanitized_text = sanitize(text)
remove_duplicates(sanitized_text)