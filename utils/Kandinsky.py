import replicate
import pathlib as pl
import json

class Replica:
    def __init__(self, url='kandinsky-2'):
        urls = {'kandinsky-2': 'ai-forever/kandinsky-2:601eea49d49003e6ea75a11527209c4f510a93e2112c969d548fbb45b9c4f19f',
                'stable-diffusion': 'stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf'}
        path = pl.Path(pl.Path.cwd(),'keys.json')
        with open(path) as keys_file:
            data = json.load(keys_file)
            
        self.client = replicate.Client(api_token=data['replica-token'])
        self.url = urls.get(url)
    
    def imagine(self, prompt):
        output = self.client.run(
            self.url,
            input={"prompt": prompt}
        )
        return output