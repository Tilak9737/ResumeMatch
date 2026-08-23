import json

def validate_skills():
    with open("data/skills.json", "r") as f:
        skills = json.load(f)
        
    canonical_names = set()
    all_aliases = {}
    
    errors = []
    
    for key, data in skills.items():
        canonical = data.get("canonical")
        aliases = data.get("aliases", [])
        category = data.get("category")
        parent = data.get("generic_parent")
        
        if not canonical:
            errors.append(f"Missing canonical name for key: {key}")
        elif canonical in canonical_names:
            errors.append(f"Duplicate canonical name found: {canonical}")
        else:
            canonical_names.add(canonical)
            
        if not category:
            errors.append(f"Missing category for: {canonical}")
            
        if not parent:
            errors.append(f"Missing generic_parent for: {canonical}")
            
        if not aliases:
            errors.append(f"Empty aliases for: {canonical}")
            
        for alias in aliases:
            if alias in all_aliases:
                errors.append(f"Alias collision! '{alias}' belongs to both '{all_aliases[alias]}' and '{canonical}'")
            else:
                all_aliases[alias] = canonical
                
    if errors:
        for e in errors:
            print("ERROR:", e)
        print(f"Validation FAILED with {len(errors)} errors.")
    else:
        print(f"Validation PASSED. {len(skills)} skills are perfectly formatted.")

if __name__ == "__main__":
    validate_skills()
