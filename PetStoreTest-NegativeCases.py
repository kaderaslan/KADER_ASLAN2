
import requests
import json
from functools import partial

# Base URL
BASE_URL = "https://petstore.swagger.io/v2"

##########################################################################################################################
# Negative Test: Attempt to read a non-existent pet

def get_pet_with_large_id():
    url = f"{BASE_URL}/pet/999999999999999"  # Çok büyük bir pet ID
    response = requests.get(url)
    print(f"Get Pet with Large ID Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response


def get_pet_with_invalid_id_type():
    url = f"{BASE_URL}/pet/abc123"  # Geçersiz pet ID (String)
    response = requests.get(url)
    print(f"Get Pet with Invalid ID Type Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response


def get_pet_invalid_json_format():
    url = f"{BASE_URL}/pet/12345"  # Geçerli pet ID, ancak yanlış formatta bir istek gönderiyoruz
    response = requests.get(url, headers={"Content-Type": "application/xml"})  # Geçersiz Content-Type
    print(f"Get Pet with Invalid JSON Format Status Code: {response.status_code}")
    print(f"Response: {response.text}")  # response.text çünkü JSON hatası olabilir
    return response

def get_pet_with_invalid_authorization():
    url = f"{BASE_URL}/pet/12345"
    headers = {
        "Authorization": "Bearer invalid_token"  # Geçersiz token
    }
    response = requests.get(url, headers=headers)
    print(f"Get Pet with Invalid Authorization Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response

# Eğer API, boş ID ile bir GET isteği kabul etmiyorsa, 405 Method Not Allowed dönecektir.
# Yanıt geçerli bir JSON değilse, ValueError hatasını yakalayarak uygun bir mesaj gösteriyoruz.
def get_pet_with_empty_id():
    url = f"{BASE_URL}/pet/"  # ID eksik
    response = requests.get(url)

    print(f"Get Pet with Empty ID Status Code: {response.status_code}")

    # Hata durumunu kontrol et
    if response.status_code == 405:
        print("Error: Method Not Allowed for empty ID")
    elif response.status_code == 404:
        print("Error: Pet not found")
    else:
        try:
            print(f"Response: {response.json()}")
        except ValueError:
            print("Response is not in valid JSON format.")

    return response


def get_pet_with_invalid_query_param():
    url = f"{BASE_URL}/pet"
    params = {"status": "nonexistent_status"}  # Geçersiz query parametresi
    response = requests.get(url, params=params)

    print(f"Get Pet with Invalid Query Param Status Code: {response.status_code}")

    # Hata durumunu kontrol et
    if response.status_code == 405:
        print("Error: Method Not Allowed for invalid query parameter")
    else:
        # JSON çözümleme hatasını önlemek için yanıtı kontrol et
        try:
            print(f"Response: {response.json()}")
        except ValueError:
            print("Response is not in valid JSON format or empty.")

    return response


def get_pet_with_empty_authorization():
    url = f"{BASE_URL}/pet/12345"
    headers = {
        "Authorization": ""  # Boş token
    }
    response = requests.get(url, headers=headers)
    print(f"Get Pet with Empty Authorization Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response


def get_pet_with_invalid_content_type():
    url = f"{BASE_URL}/pet/12345"
    headers = {
        "Content-Type": "application/xml"  # Geçersiz Content-Type
    }
    response = requests.get(url, headers=headers)
    print(f"Get Pet with Invalid Content-Type Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response


def create_pet_with_invalid_id():
    url = f"{BASE_URL}/pet"
    invalid_pet_data = {
        "id": '0,5',  # Geçersiz ID (negatif sayı)
        "name": "doggie",
        "status": "available",
        "category": {
            "id": 1,
            "name": "dog"
        },
        "tags": [{"id": 1, "name": "friendly"}],
        "photoUrls": ["url1"]
    }

    response = requests.post(url, data=json.dumps(invalid_pet_data), headers={"Content-Type": "application/json"})
    print(f"Create Pet with Invalid ID Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response


def create_pet_missing_name():
    url = f"{BASE_URL}/pet"
    invalid_pet_data = {
        "id": 12345,
        "status": "available",  # name alanı eksik
        "category": {
            "id": 1,
            "name": "dog"
        },
        "tags": [{"id": 1}],
        "photoUrls": ["url1"]
    }

    response = requests.post(url, data=json.dumps(invalid_pet_data), headers={"Content-Type": "application/json"})
    print(f"Create Pet Missing Name Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response


def create_pet_invalid_json_format():
    url = f"{BASE_URL}/pet"
    invalid_pet_data = "{ 'id': 12345, 'name': 'doggie', 'status': 'available' }"  # Hatalı JSON formatı (tek tırnaklar)

    response = requests.post(url, data=invalid_pet_data, headers={"Content-Type": "application/json"})
    print(f"Create Pet with Invalid JSON Format Status Code: {response.status_code}")
    print(f"Response: {response.text}")  # response.text kullanılır çünkü JSON hatası olabilir
    return response

def create_pet_invalid_category_id():
    url = f"{BASE_URL}/pet"
    invalid_pet_data = {
        "id": 12345,
        "name": "doggie",
        "status": "available",
        "category": {
            "id": 'abcd',  # Geçersiz kategori ID
            "name": "dog"
        },
        "tags": [{"id": 1, "name": "friendly"}],
        "photoUrls": ["url1"]
    }

    response = requests.post(url, data=json.dumps(invalid_pet_data), headers={"Content-Type": "application/json"})
    print(f"Create Pet with Invalid Category ID Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response


def create_pet_malformed_json():
    url = f"{BASE_URL}/pet"
    malformed_json = '{"id": 12345, "name": "doggie", "status": "available",}'  # Trailing comma makes it invalid
    response = requests.post(url, data=malformed_json, headers={"Content-Type": "application/json"})
    print(f"Create Pet Malformed JSON Status Code: {response.status_code}")
    print(f"Response: {response.text}")  # Invalid JSON will not parse
    return response


def create_pet_invalid_data_types():
    url = f"{BASE_URL}/pet"
    invalid_pet_data = {
        "id": "invalid_id",  # Should be an integer
        "name": 12345,       # Should be a string
        "status": True,      # Should be a string
        "photoUrls": "invalid_url",  # Should be a list
    }
    response = requests.post(url, data=json.dumps(invalid_pet_data), headers={"Content-Type": "application/json"})
    print(f"Create Pet Invalid Data Types Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response


def create_pet_invalid_content_type():
    url = f"{BASE_URL}/pet"
    valid_pet_data = {
        "id": 12345,
        "name": "doggie",
        "photoUrls": ["string"],
        "status": "available"
    }
    response = requests.post(url, data=json.dumps(valid_pet_data), headers={"Content-Type": "text/plain"})
    print(f"Create Pet Invalid Content-Type Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    return response

def create_pet_empty_photoUrls():
    url = f"{BASE_URL}/pet"
    invalid_pet_data = {
        "id": 12345,
        "name": "doggie",
        "status": "available",
        "category": {
            "id": 1,
            "name": "dog"
        },
        "tags": [{"id": 1, "name": "friendly"}],
        "photoUrls":{}  # Empty array
    }
    response = requests.post(url, data=json.dumps(invalid_pet_data), headers={"Content-Type": "application/json"})
    print(f"Create Pet Empty PhotoUrls Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response

def update_pet_with_invalid_id():
    pet_id = 0,99999999  # Var olmayan bir Pet ID
    url = f"{BASE_URL}/pet"
    pet_data = {
        "id": pet_id,
        "name": "Tommy Updated",
        "status": "sold",
        "category": {
            "id": 1,
            "name": "dog"
        },
        "tags": [{"id": 1, "name": "playful"}]
    }
    response = requests.put(url, data=json.dumps(pet_data), headers={"Content-Type": "application/json"})
    print(f"Update Pet with Invalid ID Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response

def update_pet_with_invalid_id_format():
    pet_id = "invalid_id"  # Geçersiz Pet ID formatı (String yerine tam sayı)
    url = f"{BASE_URL}/pet"
    pet_data = {
        "id": pet_id,
        "name": "Tommy Updated",
        "status": "sold",
        "category": {
            "id": 1,
            "name": "dog"
        },
        "tags": [{"id": 1, "name": "playful"}]
    }
    response = requests.put(url, data=json.dumps(pet_data), headers={"Content-Type": "application/json"})
    print(f"Update Pet with Invalid ID Format Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response


def update_pet_with_missing_field():
    pet_id = 12345
    url = f"{BASE_URL}/pet"
    pet_data = {
        "id": pet_id,
        # "name" alanı eksik
        "status": "available",  # Ancak, 'name' eksik
    }
    response = requests.put(url, data=json.dumps(pet_data), headers={"Content-Type": "application/json"})

    print(f"Update Pet with Missing Field Status Code: {response.status_code}")

    # Yanıtın eksik alanla geldiğini kontrol et
    if response.status_code == 200:
        print("Unexpected response: Missing required fields should return an error.")
    else:
        print(f"Response: {response.json()}")  # Eğer API doğru hata mesajı döndürebildiyse burada görünür

    return response


def update_pet_with_invalid_status_value():
    pet_id = 12345
    url = f"{BASE_URL}/pet"
    pet_data = {
        "id": pet_id,
        "name": "Tommy Updated",
        "status": "invalid_status",  # Geçersiz status değeri
        "category": {
            "id": 1,
            "name": "dog"
        },
        "tags": [{"id": 1, "name": "playful"}]
    }
    response = requests.put(url, data=json.dumps(pet_data), headers={"Content-Type": "application/json"})

    print(f"Update Pet with Invalid Status Value Status Code: {response.status_code}")

    # Yanıtın geçersiz değerle geldiğini kontrol et
    if response.status_code == 200:
        print("Unexpected response: Invalid status should return an error.")
    else:
        print(f"Response: {response.json()}")  # Eğer API doğru hata mesajı döndürebildiyse burada görünür

    return response


def update_pet_with_invalid_json_format():
    pet_id = 12345  # Geçerli bir Pet ID
    url = f"{BASE_URL}/pet"
    pet_data = {
        "id": pet_id,
        "name": "Tommy Updated",
        "status": "sold",
        "category": {
            "id": 1,
            "name": "dog"
        },
        "tags": [{"id": 1, "name": "playful"}]
    }
    response = requests.put(url, data="<xml>invalid data</xml>", headers={"Content-Type": "application/xml"})
    print(f"Update Pet with Invalid JSON Format Status Code: {response.status_code}")
    print(f"Response: {response.text}")  # response.text çünkü JSON hatası olabilir
    return response

# id random bir değer yaratılıyor
def update_pet_with_empty_id():
    pet_id = ""  # Boş ID
    url = f"{BASE_URL}/pet"
    pet_data = {
        "id": pet_id,  # Boş ID
        "name": "Tommy Updated",
        "status": "sold",
        "category": {
            "id": 1,
            "name": "dog"
        },
        "tags": [{"id": 1, "name": "playful"}]
    }
    response = requests.put(url, data=json.dumps(pet_data), headers={"Content-Type": "application/json"})

    print(f"Update Pet with Empty ID Status Code: {response.status_code}")

    # Yanıtın boş ID ile geldiğini kontrol et
    if response.status_code == 200:
        print("Unexpected response: Pet ID should not be empty.")
    else:
        print(f"Response: {response.json()}")  # Eğer API doğru hata mesajı döndürebildiyse burada görünür

    return response

def update_pet_with_invalid_header():
    pet_id = 12345  # Geçerli bir Pet ID
    url = f"{BASE_URL}/pet"
    pet_data = {
        "id": pet_id,
        "name": "Tommy Updated",
        "status": "sold",
        "category": {
            "id": 1,
            "name": "dog"
        },
        "tags": [{"id": 1, "name": "playful"}]
    }
    response = requests.put(url, data=json.dumps(pet_data), headers={"Content-Type": "application/xml"})  # Yanlış Content-Type
    print(f"Update Pet with Invalid Header Status Code: {response.status_code}")
    print(f"Response: {response.text}")  # response.text çünkü JSON hatası olabilir
    return response


def update_pet_with_invalid_id():
    pet_data = {
        "id": 9999999999999999999999999999999999999999999999,  # Geçersiz ID
        "name": "Tommy Updated",
        "status": "sold",
        "category": {"id": 1, "name": "dog"},
        "tags": [{"id": 1, "name": "playful"}],
        "photoUrls": ["http://example.com/photo.jpg"]
    }

    url = f"{BASE_URL}/pet"
    response = requests.put(url, data=json.dumps(pet_data), headers={"Content-Type": "application/json"})

    print(f"Update Pet Response Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    return response


def get_pet_with_invalid_endpoint():
    url = f"{BASE_URL}/invalid_endpoint"  # Hatalı URL
    response = requests.get(url)

    print(f"Response invalid endpoint Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    return response


# Negative Test: Delete a non-existent pet
def delete_non_existent_pet():
    pet_id = 99999999999999  # Non-existent pet ID
    url = f"{BASE_URL}/pet/{pet_id}"
    response = requests.delete(url)
    print(f"Delete Non-Existent Pet Status Code: {response.status_code}")
    if response.status_code == 404:
        print("Expected result: Pet not found.")
    else:
        print(f"Unexpected Response: {response.json()}")
    return response

# Negative Test: Delete with invalid pet ID
def delete_invalid_pet_id():
    pet_id = "invalid_id"  # Invalid pet ID (string instead of numeric)
    url = f"{BASE_URL}/pet/{pet_id}"
    response = requests.delete(url)
    print(f"Delete Invalid Pet ID Status Code: {response.status_code}")
    if response.status_code == 400:
        print("Expected result: Bad Request due to invalid ID.")
    else:
        print(f"Unexpected Response: {response.json()}")
    return response



def upload_pet_image_invalid_pet_id(pet_id, file_path):
    url = f"{BASE_URL}/pet/{pet_id}/uploadImage"
    files = {"file": open(file_path, "rb")}
    response = requests.post(url, files=files)
    print(f"Invalid Pet ID - Status Code: {response.status_code}")
    if response.status_code == 404:
        print("Pet not found!")
    else:
        print(f"Unexpected status: {response.status_code}")
    return response




def upload_pet_image_invalid_file_path(pet_id, file_path):
    try:
        url = f"{BASE_URL}/pet/{pet_id}/uploadImage"
        files = {"file": open(file_path, "rb")}
        response = requests.post(url, files=files)
        print(f"Invalid File Path - Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
        return response
    except FileNotFoundError:
        print("File not found!")


def upload_pet_image_unsupported_file(pet_id, file_path):
    url = f"{BASE_URL}/pet/{pet_id}/uploadImage"
    files = {"file": open(file_path, "rb")}
    response = requests.post(url, files=files)
    print(f"Unsupported File Type - Status Code: {response.status_code}")
    if response.status_code == 415:
        print("Unsupported media type!")
    else:
        print(f"Unexpected status: {response.status_code}")
    return response


def upload_pet_image_large_file(pet_id, file_path):
    url = f"{BASE_URL}/pet/{pet_id}/uploadImage"
    files = {"file": open(file_path, "rb")}
    response = requests.post(url, files=files)
    print(f"File Too Large - Status Code: {response.status_code}")
    if response.status_code == 413:
        print("File size exceeds limit!")
    else:
        print(f"Unexpected status: {response.status_code}")
    return response


def update_pet_status_invalid_pet_id(pet_id, new_status):
    url = f"{BASE_URL}/pet"
    pet_data = {
        "id": pet_id,
        "status": new_status,
    }
    response = requests.put(url, data=json.dumps(pet_data), headers={"Content-Type": "application/json"})
    print(f"Invalid Pet ID - Status Code: {response.status_code}")
    if response.status_code == 404:
        print("Pet not found!")
    else:
        print(f"Unexpected status: {response.status_code}")
    return response

def update_pet_status_invalid_status(pet_id, new_status):
    url = f"{BASE_URL}/pet"
    pet_data = {
        "id": pet_id,
        "status": new_status,  # Invalid status (e.g., "not_active")
    }
    response = requests.put(url, data=json.dumps(pet_data), headers={"Content-Type": "application/json"})
    print(f"Invalid Status - Status Code: {response.status_code}")
    if response.status_code == 400:
        print("Invalid status provided!")
    else:
        print(f"Unexpected status: {response.status_code}")
    return response

def update_pet_status_missing_fields(pet_id, new_status):
    url = f"{BASE_URL}/pet"
    # Missing 'id' or 'status' field
    pet_data = {
        "id": pet_id,  # For missing 'status'
        # "status": new_status,  # Uncomment to test missing 'status'
    }
    response = requests.put(url, data=json.dumps(pet_data), headers={"Content-Type": "application/json"})
    print(f"Missing Fields - Status Code: {response.status_code}")
    if response.status_code == 400:
        print("Missing required fields!")
    else:
        print(f"Unexpected status: {response.status_code}")
    return response

def update_pet_status_invalid_json(pet_id, new_status):
    url = f"{BASE_URL}/pet"
    # Incorrectly formatted JSON (e.g., missing closing brace)
    pet_data = '{"id": ' + str(pet_id) + ', "status": "' + new_status + '"'
    response = requests.put(url, data=pet_data, headers={"Content-Type": "application/json"})
    print(f"Invalid JSON Format - Status Code: {response.status_code}")
    if response.status_code == 400:
        print("Malformed JSON in request!")
    else:
        print(f"Unexpected status: {response.status_code}")
    return response


def run_test_cases(test_cases):
    """
    Test case isimlerini alır, sırayla çalıştırır ve sonuçları konsola yazar.

    Args:
        test_cases (list): Çalıştırılacak test case fonksiyonlarının isimlerinden oluşan liste.
    """
    for test in test_cases:
        # Eğer test bir partial ise, custom bir isim kullan
        test_name = test.func.__name__ if isinstance(test, partial) else test.__name__
        print(f"\nÇalıştırılıyor: {test_name}")
        try:
            test()  # Test fonksiyonunu çalıştır
            print(f"{test_name} başarıyla tamamlandı.")
        except Exception as e:
            print(f"Hata: {test_name} başarısız oldu. Hata: {e}")

def get_test_cases():
    """
    Çalıştırılacak tüm test caselerini bir liste olarak döner.

    Returns:
        list: Test case fonksiyonlarının bir listesi.
    """
    return [
        get_pet_with_large_id,
        get_pet_with_invalid_id_type,
        get_pet_invalid_json_format,
        get_pet_with_invalid_authorization,
        get_pet_with_empty_id,
        get_pet_with_invalid_query_param,
        get_pet_with_empty_authorization,
        get_pet_with_invalid_content_type,
        create_pet_malformed_json,
        create_pet_invalid_data_types,
        create_pet_invalid_content_type,
        create_pet_empty_photoUrls,
        create_pet_with_invalid_id,
        create_pet_missing_name,
        create_pet_invalid_json_format,
        create_pet_invalid_category_id,
        update_pet_with_invalid_id,
        update_pet_with_invalid_id_format,
        update_pet_with_missing_field,
        update_pet_with_invalid_status_value,
        update_pet_with_invalid_json_format,
        update_pet_with_empty_id,
        update_pet_with_invalid_header,
        update_pet_with_invalid_id,
        get_pet_with_invalid_endpoint,
        delete_non_existent_pet,
        delete_invalid_pet_id,
        partial(upload_pet_image_invalid_pet_id,9999990009, "pets-3715733_1280.jpg"),
        partial(upload_pet_image_invalid_file_path,123, "nonexistent_image.jpg"),
        partial(upload_pet_image_unsupported_file,123, "image.txt"),
        partial(upload_pet_image_large_file,123, "large_image.jpg"),
        partial(update_pet_status_invalid_pet_id,99999, "sold"),
        partial(update_pet_status_invalid_status,12345, "not_active"),
        partial(update_pet_status_missing_fields,""),
        partial(update_pet_status_invalid_json,123, "sold")
    ]

if __name__ == "__main__":
    print("Testler Başlatılıyor...\n")
    test_case_list = get_test_cases()
    run_test_cases(test_case_list)
    print("\nTüm testler tamamlandı.")