import requests

BASE_URL = "https://api.flyff.com"


def get_monsters_ids():
    return requests.get(f"{BASE_URL}/monster").json()


def get_monsters_by_ids(monster_ids):
    ids_string = ",".join(map(str, monster_ids))
    response = requests.get(f"{BASE_URL}/monster", params={"id": ids_string})

    try:
        result = response.json()
        if isinstance(result, list):
            return result
        else:
            print(f"Unexpected response format: {result}")
            return []
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        return []


def simplify_monster(monster):
    if not isinstance(monster, dict):
        return None  # skip if it's not a valid monster object

    return {
        "id": monster.get("id"),
        "name": monster.get("name", {}).get("en", "Unknown"),
        "level": monster.get("level"),
        "hp": monster.get("hp"),
        "attack": monster.get("attack"),
        "defense": monster.get("defense"),
    }


def get_all_monsters_english(batch_size=50):
    monster_ids = get_monsters_ids()
    all_monsters = []

    for i in range(0, len(monster_ids), batch_size):
        batch = monster_ids[i:i+batch_size]
        monsters_batch = get_monsters_by_ids(batch)

        if isinstance(monsters_batch, list):
            all_monsters.extend([
                m for m in (simplify_monster(monster) for monster in monsters_batch)
                if m is not None
            ])
        else:
            print(f"Error fetching batch: {batch}")

    return all_monsters


if __name__ == "__main__":
    monsters = get_all_monsters_english()
    print(f"Total Monsters Retrieved: {len(monsters)}")
    for m in monsters[:10]:
        print(m)
