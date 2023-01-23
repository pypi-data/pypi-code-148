import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from getpass import getpass



class raphael: 
    photo=''
    regno=''
    gender=''
    dob=''
    email=''
    mobile=''
    martial_status=''
    academic_year=''
    NTA_level=''
    name=''
    nationality = ''
    sem1=''
    sem2=''
    total_results=''
    GPA_sem1=''
    GPA_sem2=''
    GPA_sem1_status=''
    GPA_sem2_status=''
    overall_GPA=''
    overall_status=''
    sem1_csv=''
    sem2_csv=''
    overall_sem_csv=''
    error = ''
    level =""
    
    
    
    def result(self,email, password):
        self.sem1,
        self.sem2, 
        self.total_results,
        self.sem1_csv,
        self.sem2_csv, 
        self.overall_sem_csv,
        self.GPA_sem1=''
        self.GPA_sem2=''
        self.GPA_sem1_status=''
        self.GPA_sem2_status=''
        self.overall_GPA=''
        self.overall_status=''
       
        
        
        try:
            login_url = 'https://soma.dit.ac.tz/login'
            secure_url = 'https://soma.dit.ac.tz/'
            session = requests.Session()
            secure_url = 'https://soma.dit.ac.tz/'
            request = session.get(login_url).content

            soup = bs(request,'html.parser')

            csrf = soup.find('input',{'name':'csrf'}).get('value')

            payload = {
                    'email': email,
                    'password': password,
                    'csrf': csrf,  

                    }


            p = session.post(login_url,data=payload)
            if 'Welcome, you have successfully logged into your account' in p.text:
                print('login successful')
                t = session.get(secure_url)
                
                soup = bs(t.text, "html.parser")

                link =soup.select('a.nav-link')
                links = [ links.get("href") for links in link] 
                result_url = [l for l in links if '/student-semester-results' in l]
                
                result_url = (f'https://soma.dit.ac.tz{result_url[0]}')
                total_result = session.get(result_url).text
                
                self.total_results= pd.read_html(total_result)
                
                total_result = bs(total_result,'html.parser')
                self.sem1 = pd.DataFrame(self.total_results[0])
                #self.sem1.to_csv('matokeo_sem1.csv',index=False)

                self.sem2 = pd.DataFrame(self.total_results[1])
                
                sem_pga = total_result.find_all('h6')
                sem_pga_total = total_result.find_all('h5')
                h6 = []
                h5=[]
                
                for sem_pga in sem_pga:
                    h6.append(sem_pga.text.strip())
                    
                self.GPA_sem1 = h6[2].split(':')[1][1:5].strip()
                self.GPA_sem1_status = (h6[2].split(':')[1][-4:].strip())
                self.GPA_sem2_status = h6[3].split(':')[1][-4:].strip()
                self.GPA_sem2 = h6[3].split(':')[1][1:5].strip()
                
                for sem in sem_pga_total:
                    h5.append(sem.text.strip())
                self.overall_GPA=(h5[0][-5:].strip())
                self.overall_status = (h5[1][-5:].strip())
                
                #self.sem2.to_csv('matokeo_sem2.csv',index=False)

                #sem1 = pd.read_csv('matokeo_sem1.csv')
                
                #sem2= pd.read_csv('matokeo_sem2.csv')
                
                #self.overall_sem_csv = pd.merge(sem1,sem2, how='outer')
                #self.overall_sem_csv.to_csv('matokeo.csv', index=False)
            elif 'invalid' in p.text:
                print('Login Failed: invalid credentials'+ str(p.status_code))
            else:
                print('invalid status code') 
        except:
            print('no internet connection')


    


   
    def studentInfo(self,email, password):
        self.name
        self.email 
        self.mobile,
        self.martial_status
        self.nationality,
        self.gender
        self.dob
        self.academic_year
        self.NTA_level
        self.regno
        self.error
        self.level
        try:
            login_url = 'https://soma.dit.ac.tz/login'
            secure_url = 'https://soma.dit.ac.tz/'
            session = requests.Session()
            secure_url = 'https://soma.dit.ac.tz/'
            request = session.get(login_url).content

            soup = bs(request,'html.parser')

            csrf = soup.find('input',{'name':'csrf'}).get('value')

            payload = {
                    'email': email,
                    'password': password,
                    'csrf': csrf,  

                    }


            p = session.post(login_url,data=payload)
            if 'Welcome, you have successfully logged into your account' in p.text:
                print('successful login')

                t = session.get(secure_url)

                soup = bs(t.text, "html.parser")

                link =soup.select('a.nav-link')
                links = [ links.get("href") for links in link] 
                
                
                person_info = [p for p in links if '/student-profile-registration' in p]


                person_info = (f'https://soma.dit.ac.tz/{person_info[0]}')
                person_info = session.get(person_info).text

                
                soup = bs(person_info,'html.parser')
                self.name = soup.find(class_='profile-username text-center').text
                
                self.regno = soup.find(class_='text-muted text-center').find('strong').text.rstrip()
            
            
                info = soup.select('li.list-group-item')

                content =  []
                for tag in info:
                    tag = tag.find(class_="float-right").text.rstrip()
                    content.append(tag)

            
                self.gender =  content[0]
                self.dob =  content[1]

            

                level = soup.select('p.text-muted')
                self.level = level[-1].text.strip().replace("   "," ")
      
                self.email = soup.find('input',{'name':'email'}).get('value')
                self.mobile = soup.find('input',{'name':'phone_number'}).get('value')
                self.martial_status = soup.find(id='marital_status_id').find('option',selected=True).text.strip()

                self.nationality = soup.find(id='nationality_id').find('option',selected=True).text.strip()
            

                academic_info = [p for p in links if '/admission/registrationct' in p]
                academic_info = (f'https://soma.dit.ac.tz/{academic_info[0]}')
                academic_info = session.get(academic_info).text
                soup = bs(academic_info,'html.parser')

                self.academic_year = soup.find('h4').text.strip()[-9:]
                

                module_link = soup.find_all('a')[-3].get("href")
                module = (f'https://soma.dit.ac.tz{module_link}')

                module = session.get(module).text
                modules = pd.read_html(module)[0]
                modules = pd.DataFrame(modules)
                self.NTA_level = (modules['Code'][0][5])
                
                
                
            elif 'invalid' in p.text:
               self.error = 'Login Failed: invalid credentials'
            else:
                self.error = 'invalid status code' 
        except:
            self.error = 'no internet connection'

    def studentImage(self,email,password):
        
        self.regno
        self.photo
        self.error
        try:  
            login_url = 'https://soma.dit.ac.tz/login'
            secure_url = 'https://soma.dit.ac.tz/'
            session = requests.Session()
            secure_url = 'https://soma.dit.ac.tz/'
            request = session.get(login_url).content

            soup = bs(request,'html.parser')

            csrf = soup.find('input',{'name':'csrf'}).get('value')

            payload = {
                    'email': email,
                    'password': password,
                    'csrf': csrf,  

                    }


            p = session.post(login_url,data=payload)
            if 'Welcome, you have successfully logged into your account' in p.text:
                print('successful login')

                t = session.get(secure_url)

                soup = bs(t.text, "html.parser")

                link =soup.select('a.nav-link')
                links = [ links.get("href") for links in link] 
                
                
                person_info = [p for p in links if '/student-profile-registration' in p]


                person_info = (f'https://soma.dit.ac.tz/{person_info[0]}')
                person_info = session.get(person_info).text

                
                soup = bs(person_info,'html.parser')
                self.regno = soup.find(class_='text-muted text-center').find('strong').text.rstrip()
                image =  soup.find(class_='profile-user-img img-fluid img-circle').get('src')

                image_url = secure_url+image[1:]
                image_response = session.get(image_url)

                ##save the image
                
                self.photo = open(f"{self.regno}.jpg", "wb").write(image_response.content)
            
            elif 'invalid' in p.text:
               self.error = 'Login Failed: invalid credentials'
            else:
                self.error = 'invalid status code' 
        except:
            self.error = 'no internet connection'
                
rex=raphael()

