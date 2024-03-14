import sys


def calculate_price_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            num_characters = len(content)
            price_cents = (num_characters / 1000000) * 1500
            return {"success": True, "num_characters": num_characters, "price_cents": price_cents}
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    result = calculate_price_from_file(file_path)

    if result["success"]:
        print(f"Number of characters: {result['num_characters']}")
        print(f"Price: {result['price_cents']:.2f} cents")
    else:
        print(f"Error reading file: {result['error']}")
