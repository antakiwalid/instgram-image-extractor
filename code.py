import requests, os, re, json

os.chdir("C:/Users/walidantaki/Desktop")





class Instgram_pic_extractor:

    instgram = "https://www.instagram.com"
    query_url = "https://www.instagram.com/graphql/query"
    display_urls = []
    data = {
        'query_hash' : 'f2405b236d85e8296cf30347c9f08c2a',
        "after":"QVFBRHBtNDZ1dm5VaExSVG9zQ3Z1YWhSWU54WVVjMHc3eW5TWTIxX2sya1RoQnZ0Z3p5LUJUdUFOYzc5SUNURDY5WXl6cTN5aFRGR2NPYTY3NlYxeGNpdw=="
    }

    def __init__(self, num_of_extractions, profile_handle, directory_name):
        self.profile_handle = profile_handle
        self.directory_name = directory_name
        self.data['id'] = self.get_userid()
        try:
            os.mkdir(directory_name)
        except FileExistsError:
            pass

        self.get_first12()
        if num_of_extractions <= 12:
            self.display_urls = self.display_urls[:num_of_extractions]
        else:
            self.get_after12(num_of_extractions - 12)
        self.write_to_file()

    def get_first12(self):
        response = requests.get(self.instgram + '/' + self.profile_handle)
        profile_html = response.text
        results = re.findall('"display_url":"(.*?)"', profile_html)[2:]
        self.display_urls.extend(results)
    

    def get_after12(self, n):
        self.data['first'] = n
        response = requests.get(self.query_url, params = self.data)
        response_json = response.json()
        edges = response_json['data']['user']['edge_owner_to_timeline_media']['edges']
        for node in edges:
            self.display_urls.append(node['node']['display_url'])
        
    def get_userid(self):
        response = requests.get(self.instgram + '/' + self.profile_handle + '/?__a=1')
        res_json = response.json()
        user_id = res_json['graphql']['user']['id']
        return user_id


    def write_to_file(self):
        for i in range(len(self.display_urls)):
            pic = self.display_urls[i]
            with open(self.directory_name + '/' + str(i) + '.jpg', 'wb') as f:
                response = requests.get(pic)
                f.write(response.content) 


profile_handle = input('profile : ')
num_of_extractions = input('number of pictures to extract : ')
directory_name = input('directory : ')
Instgram_pic_extractor(int(num_of_extractions), profile_handle, directory_name)