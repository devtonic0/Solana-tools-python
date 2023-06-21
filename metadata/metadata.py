import json
import urllib.request
from tqdm import tqdm

# Define the dictionary of replacement values
replace_dict = {
"Beige" : "Beige",
"Green" : "Light Green",
"Lilac" : "Lilac",
"Orange" : "Orange",
"Pink" : "Light Pink",
"Sky" : "Sky",
"Soft" : "Soft",
"Sun ray" : "Sunny Day",
"grey rare" : "Trippy Grey",
"pink rare" : "Trippy Pink",
"rare blended" : "Blended",
"Squares" : "Jagged",
"rare combo" : "Squares",
"teal rare" : "Trippy Teal",
"trippy blue" : "Trippy Blue",
"trippy purple" : "Trippy Purple",
"Sandy vest" : "Sandy Chestplate",
"advisor" : "Sheriff",
"advisor red" : "Gunslinger",
"basic chestplate" : "Armored Shirt",
"basic tshirt" : "Basic T-shirt",
"black hole shirt" : "Black Hole Shirt",
"bonk brown" : "Bonk Brown",
"bonk orange" : "Bonk Orange",
"brown chestplate with chain" : "Brown Chestplate with Chain",
"brown shirt with tee" : "Worker Overalls",
"gold chestplate" : "Golden Mantle",
"green priest robe" : "Nobleman",
"hoodie brown" : "Brown Hoodie",
"Vendetta" : "Vendetta",
"ancient" : "Ancient",
"black hole" : "Black Holes",
"blue zombie" : "Blue Zombie",
"crystal" : "Brown Crystal",
"curious" : "Curious",
"dollar signs" : "Dollar Signs",
"green angry" : "Green Angry",
"harry potter" : "Harry Potter",
"mutated" : "Mutated",
"rave" : "Rave",
"red angry" : "Red Angry",
"red crystal" : "Red Crystal",
"red zombie" : "Red Zombie",
"side eye" : "Cross-eyed",
"sunglasses" : "Sun Glasses",
"suspicious" : "Suspicious",
"teary eyed" : "Crying",
"trippy" : "Trippy",
"wood glasses" : "Steampunk",
"hoodie green" : "Green Hoodie",
"kings suit" : "Royal Robe",
"knights armor" : "Brown Warrior Armor",
"knights vest red" : "Fancy Red Outfit",
"maroon jacket" : "Puffer Jacket",
"orange vest with chain" : "Orange Vest with Chain",
"pharaoh" : "Pharaoh",
"plaid jacket with chain" : "Plaid Jacket with Chain",
"purple vest" : "Purple Chestplate",
"rare chestplate" : "Ornamental Chestplate",
"red priest robe" : "Wanderer",
"robe" : "Advisor",
"robe with chain" : "Guardian",
"shirt green" : "Green Shirt",
"shirt yellow" : "Yellow Shirt",
"stormtrooper purple" : "Purple Stormtrooper",
"suit blue" : "Blue Suit",
"suit cream" : "Cream Suit",
"toga" : "Toga",
"knights vest" : "Fancy Green Outfit",
"knights armor red"	: "Red Warrior Armor",
"stormtrooper red"	: "Red Stormtrooper",
"trainers chestplate" : "Composite Armor",
"tshirt with chain" : "T-shirt with Chain",
"turtleneck" : "Collar Jacket",
"wavy tshirt" : "Wavy T-shirt",
"yellow tshirt" : "Yellow T-shirt",
"blue cracked" : "Ice",
"brown" : "Brown",
"cream" : "Cream",
"gold" : "Gold",
"lava" : "Lava",
"oak" : "Oak",
"orange" : "Orange",
"pink wavy" : "Pink",
"purple wavy" : "Purple",
"white" : "White",
"OMG sticker" : "OMG sticker",
"axe" : "Axe",
"axe in brain" : "Axe in Brain",
"baseball hat brown" : "Brown Baseball Hat",
"baseball hat red" : "Red Baseball Hat",
"beanie" : "Beanie",
"Party Heart" : "Party Hat",
"black hole" : "Black Hole",
"brain" : "Brain",
"cowboy hat brown" : "Brown Cowboy Hat",
"cowboy hat green" : "Green Cowboy Hat",
"crown" : "Jester Hat",
"halo" : "Halo",
"heart sticker" : "Heart Sticker",
"kings crown" : "Crown",
"metal" : "Metal Brace",
"mushroom" : "Mushroom",
"none" : "None",
"sewing pin" : "Needle Cushion",
"closed mouth smirk" : "Smirk",
"closed smile" : "Flat",
"dracula" : "Dracula",
"gold mouth" : "Gold Mouth",
"metal" : "Robotic",
"mouth with cigarette" : "Smoker",
"multicolor teeth" : "Color Teeth",
"open mouth" : "Open Mouth",
"purple tongue" : "Tongue Out",
"resting" : "Resting",
"smile" : "Smile",
"smile with teeth" : "Broad Smile",
"smirk" : "Snarl",
"tentical" : "Tentacle",
"zipped" : "Zipped"
}
replace_trait_dict = {
    "Body" : "Base",
    "Accessories" : "Mutton Chops",
    "Headwear" : "Accessory",
    
    # Add other replacements here...
}
# Load the metadata JSON file
with open('metadata.json', 'r') as f:
    metadata = json.load(f)

# Get the total number of items to process
total_items = len(metadata)

# Initialize the progress bar
pbar = tqdm(total=total_items)

# Loop through each item in the metadata
for index, item in enumerate(metadata):
    metadata_uri = item['tokenData']['uri']
    mint_id = item['mint']

    # Download the metadata from the URI
    with urllib.request.urlopen(metadata_uri) as url:
        metadata_json = json.loads(url.read().decode())

    # Search and replace keywords
    replaced_names = []
    replaced_traits = []
    for attribute in metadata_json['attributes']:
        if attribute['value'] in replace_dict:
             new_value = replace_dict[attribute['value']]
             attribute['value'] = new_value
             replaced_names.append(f"{attribute['value']} (mint {mint_id}, {attribute['trait_type']})")

        if attribute['trait_type'] in replace_trait_dict:
            new_trait_type = replace_trait_dict[attribute['trait_type']]
            attribute['trait_type'] = new_trait_type
            replaced_traits.append(f"{new_trait_type} (mint {mint_id})")

    # Save the updated metadata as a new JSON file
    with open(f'updated_metadata/{mint_id}.json', 'w') as f:
        json.dump(metadata_json, f)
    # Update the progress bar
    pbar.update(1)
    pbar.set_description(f"Processed mint {mint_id}")
    if replaced_names or replaced_traits:
        pbar.set_postfix({'replaced names': replaced_names, 'replaced traits': replaced_traits})

# Close the progress bar
pbar.close()
