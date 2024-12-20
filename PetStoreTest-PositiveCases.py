import requests
import json
from functools import partial


# Base URL
BASE_URL = "https://petstore.swagger.io/v2"

# Positive Test: Create a Pet
def create_pet():
    url = f"{BASE_URL}/pet"
    pet_data = {
        "id": 12345,
        "name": "Tommy",
        "status": "available",
        "category": {
            "id": 1,
            "name": "dog"
        },
        "tags": [{"id": 1, "name": "friendly"}]
    }
    response = requests.post(url, data=json.dumps(pet_data), headers={"Content-Type": "application/json"})
    print(f"Create Pet Status Code: {response.status_code}")
    print(f"Create Pet Response: {response.json()}")
    return response

def create_multiple_pets():
    pets = [
        {"id": 1111, "name": "Rex", "status": "available", "category": {"id": 1, "name": "dog"}, "tags": [{"id": 1, "name": "friendly"}]},
        {"id": 2222, "name": "Whiskers", "status": "pending", "category": {"id": 2, "name": "cat"}, "tags": [{"id": 2, "name": "cute"}]},
    ]
    for pet in pets:
        response = requests.post(f"{BASE_URL}/pet", data=json.dumps(pet), headers={"Content-Type": "application/json"})
        print(f"Create Pet ID {pet['id']} Status Code: {response.status_code}")
        assert response.status_code == 200, f"Failed to create pet with ID {pet['id']}"
    print("Multiple pets created successfully.")



def create_pet_missing_fields():
    url = f"{BASE_URL}/pet"
    invalid_pet_data = {
        "id": 12345,
        "status": "available"  # Missing 'name' and 'photoUrls'
    }
    response = requests.post(url, data=json.dumps(invalid_pet_data), headers={"Content-Type": "application/json"})
    print(f"Create Pet Missing Fields Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response

def create_pet_missing_nested_fields():
    url = f"{BASE_URL}/pet"
    invalid_pet_data = {
        "id": 12345,
        "name": "doggie",
        "status": "available",
        "category": {},  # Empty category
        "tags": []  # Empty tags
    }
    response = requests.post(url, data=json.dumps(invalid_pet_data), headers={"Content-Type": "application/json"})
    print(f"Create Pet Missing Nested Fields Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response


# Positive Test: Read a Pet (GET)
def get_pet(pet_id=12345):
    url = f"{BASE_URL}/pet/{pet_id}"
    response = requests.get(url)
    print(f"Get Pet Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Pet Data: {response.json()}")
    else:
        print(f"Pet not found.")
    return response


# Positive Test: List Pets by Status (GET)
def list_pets_by_status(status='pending'):
    url = f"{BASE_URL}/pet/findByStatus?status={status}"
    response = requests.get(url)
    print(f"List Pets by Status '{status}' Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Pets List: {response.json()}")
    else:
        print("Failed to fetch pets by status.")
    return response


# Yeni oluşturulan bir pet'in detaylarını, ID ile sorgulama yaparak doğrulamak:

def verify_pet_details(pet_id=12345, expected_name="doggie", expected_status="available"):
    response = get_pet(pet_id)
    if response.status_code == 200:
        pet_data = response.json()
        assert pet_data["name"] == expected_name, "Pet name mismatch"
        assert pet_data["status"] == expected_status, "Pet status mismatch"
        print("Pet details are correct!")
    else:
        print("Pet not found for verification.")



# Positive Test: Update Pet (PUT)
def update_pet(pet_id=12345):
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
    print(f"Update Pet Status Code: {response.status_code}")
    print(f"Update Pet Response: {response.json()}")
    return response

# Positive Test: Delete a Pet (DELETE)
def delete_pet(pet_id=12345):
    url = f"{BASE_URL}/pet/{pet_id}"
    response = requests.delete(url)
    print(f"Delete Pet Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Pet Deleted Successfully")
    else:
        print(f"Error deleting pet.")
    return response


def upload_pet_image(pet_id, file_path):
    url = f"{BASE_URL}/pet/{pet_id}/uploadImage"
    files = {"file": open(file_path, "rb")}
    response = requests.post(url, files=files)
    print(f"Upload Image Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Image upload failed. Status: {response.status_code}")
    return response



def update_pet_status(pet_id, new_status):
    url = f"{BASE_URL}/pet"
    pet_data = {
        "id": pet_id,
        "status": new_status,
    }
    response = requests.put(url, data=json.dumps(pet_data), headers={"Content-Type": "application/json"})
    print(f"Update Pet Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Pet updated successfully with status: {response.json()}")
    else:
        print(f"Pet update failed. Status: {response.status_code}")
    return response



def update_pet_category(pet_id, new_category_id, new_category_name):
    url = f"{BASE_URL}/pet"
    pet_data = {
        "id": pet_id,
        "category": {
            "id": new_category_id,
            "name": new_category_name
        }
    }
    response = requests.put(url, data=json.dumps(pet_data), headers={"Content-Type": "application/json"})
    print(f"Update Pet Category Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Pet updated successfully with category: {response.json()}")
    else:
        print(f"Pet category update failed. Status: {response.status_code}")
    return response



def add_pet_tag(pet_id=12345, new_tag_name="playful"):
    url = f"{BASE_URL}/pet"
    pet_data = {
        "id": pet_id,
        "tags": [{"id": 2, "name": new_tag_name}]
    }
    response = requests.put(url, data=json.dumps(pet_data), headers={"Content-Type": "application/json"})
    print(f"Add Pet Tag Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Pet updated with new tag: {response.json()}")
    else:
        print(f"Pet tag update failed. Status: {response.status_code}")
    return response


def list_pets_by_name(name="Tommy"):
    url = f"{BASE_URL}/pet/findByStatus?status=available"
    response = requests.get(url)
    print(f"List Pets by Name '{name}' Status Code: {response.status_code}")
    if response.status_code == 200:
        pets = response.json()
        matching_pets = [pet for pet in pets if pet['name'] == name]
        print(f"Pets List with name '{name}': {matching_pets}")
    else:
        print("Failed to fetch pets by name.")
    return response


def create_multiple_and_validate_pets():
    pets = [
        {"id": 1111, "name": "Rex", "status": "available", "category": {"id": 1, "name": "dog"}, "tags": [{"id": 1, "name": "friendly"}]},
        {"id": 2222, "name": "Whiskers", "status": "pending", "category": {"id": 2, "name": "cat"}, "tags": [{"id": 2, "name": "cute"}]}
    ]
    for pet in pets:
        create_response = requests.post(f"{BASE_URL}/pet", data=json.dumps(pet), headers={"Content-Type": "application/json"})
        print(f"Create Pet ID {pet['id']} Status Code: {create_response.status_code}")
        if create_response.status_code == 200:
            created_pet_id = create_response.json().get('id')
            get_pet(created_pet_id)
        else:
            print(f"Failed to create pet with ID {pet['id']}.")


def update_pet_full_details(pet_id):
    url = f"{BASE_URL}/pet"
    pet_data = {
        "id": pet_id,
        "name": "Updated Pet Name",
        "status": "available",
        "category": {
            "id": 1,
            "name": "dog"
        },
        "tags": [{"id": 1, "name": "friendly"}]
    }
    response = requests.put(url, data=json.dumps(pet_data), headers={"Content-Type": "application/json"})
    print(f"Full Pet Update Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Updated Pet Data: {response.json()}")
    else:
        print(f"Pet update failed. Status: {response.status_code}")
    return response


def run_test_cases(test_cases):
    """
    Test case isimlerini alır, sırayla çalıştırır ve sonuçları konsola yazar.

    Args:
        test_cases (list): Çalıştırılacak test case fonksiyonlarının isimlerinden oluşan liste.
    """
    for test in test_cases:
        test_name = test.func.__name__ if isinstance(test, partial) else test.__name__
        print(f"\nÇalıştırılıyor: {test_name}")
        try:
            test()
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
        create_pet,
        create_multiple_pets,
        create_pet_missing_fields,
        create_pet_missing_nested_fields,
        get_pet,
        list_pets_by_status,
        partial(verify_pet_details,pet_id=12345, expected_name="doggie", expected_status="available"),
        update_pet,
        delete_pet,
        partial(upload_pet_image, pet_id=12345, file_path="pets-3715733_1280.jpg"),
        partial(update_pet_status,pet_id=12345, new_status="sold"),
        partial(update_pet_category,pet_id=12345, new_category_id=2, new_category_name="cat"),
        partial(add_pet_tag,pet_id=12345, new_tag_name="playful"),
        partial(list_pets_by_name,name="Tommy"),
        create_multiple_and_validate_pets,
        partial(update_pet_full_details,pet_id=12345)
    ]

if __name__ == "__main__":
    print("Testler Başlatılıyor...\n")
    test_case_list = get_test_cases()  # Test case listesini al
    run_test_cases(test_case_list)    # Listeyi çalıştır
    print("\nTüm testler tamamlandı.")