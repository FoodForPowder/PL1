import http.client
import urllib.parse
import os
import threading
import time
import sys

downloaded_kbytes = 0

def show_progress():
    global downloaded_bytes
    while True:
        print(f"Скачано КБ: {downloaded_kbytes }")
        time.sleep(1)

def get_available_filename(base_name):
   
    if not os.path.exists(base_name):
        return base_name  
    name, extension = os.path.splitext(base_name)
    counter = 1  
    while True:
        new_name = f"{name}_{counter}{extension}"
        if not os.path.exists(new_name):
            return new_name
        counter += 1

def main():
    global downloaded_kbytes
    
    url = sys.argv[1]    
    url_parts = urllib.parse.urlparse(url)
    server_name = url_parts.netloc
    file_path = url_parts.path
    
    file_name = os.path.basename(file_path)
    if file_name == "":
        file_name = "your_file"
    
    file_name = get_available_filename(file_name)
    
    progress_thread = threading.Thread(target=show_progress)
    progress_thread.daemon = True  
    progress_thread.start()
    
    try:      
        if url.startswith('https'):
            connection = http.client.HTTPSConnection(server_name)
        else:
            connection = http.client.HTTPConnection(server_name)
        
        connection.request("GET", file_path)
        
        response = connection.getresponse()
          
        if  str(response.status).startswith(("4","5")):
            print(f"Ошибка при скачивании: {response.status} {response.reason}")
            return
            
        with open(file_name, 'wb') as file:
            while True:
                
                chunk = response.read(1024)
                if not chunk:
                    break
                
              
                file.write(chunk)
                downloaded_kbytes += len(chunk) / 1024       
        print(f"\nФайл скачан и сохранен как: {file_name} {downloaded_kbytes} КБ")     
    except Exception as error:
        print(f"Произошла ошибка: {error}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()