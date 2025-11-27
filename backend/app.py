from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests
from bson import ObjectId

load_dotenv()

app = Flask(__name__)
CORS(app)

MONGO_URL = os.getenv('MONGO_URL')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

if not MONGO_URL:
    raise ValueError("MONGO_URL not found in .env file")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = MongoClient(MONGO_URL)
db = client['grant_system']
grants_collection = db['grants']

AVAILABLE_TAGS=["agriculture", "education", "STEM", "sustainability", "small business", "energy", "technology", "water", "soil", "conservation", "youth", "rural", "infrastructure", "climate", "dairy", "livestock", "equipment", "research", "training", "grant-writing"]


dummy_data =[
  {
    "grant_name": "Nutrient Management Farmer Education Grants",
    "grant_description": "The Nutrient Management Farmer Education Grant Program supports nutrient management planning in Wisconsin by funding entities to educate farmers. Its goal is to enable farmers to write their own nutrient management plans and improve their understanding of nutrient management principles. Projects focus on compliance with the 2015 NRCS 590 nutrient management plan standards.",
    "website_urls": ["https://datcp.wi.gov/Pages/Programs_Services/NMFEGrants.aspx"],
    "document_urls": ["https://datcp.wi.gov/Documents2/NMFERFA.pdf"]
  },
  {
    "grant_name": "AFID Infrastructure Program",
    "grant_description": "The AFID Infrastructure Program provides grants for community infrastructure development projects that support local food production and sustainable agriculture. These projects must demonstrate a broad community benefit and are primarily used for capital expenditures.",
    "website_urls": ["https://www.vdacs.virginia.gov/agriculture-afid-infrastructure-grants.shtml"],
    "document_urls": ["https://www.vdacs.virginia.gov/pdf/AFID-infrastructure-grant-guidelines.pdf"]
  },
  {
    "grant_name": "Local Agriculture and Seafood Act (LASA) Grants Program",
    "grant_description": "The LASA Grants Program aims to enhance the economic competitiveness of Rhode Island's agricultural products and local seafood. It provides support to farmers and organizations to develop a sustainable food system and improve marketing efforts. Eligible projects should align with the program's goals, such as marketing assistance and food safety improvements.",
    "website_urls": ["https://dem.ri.gov/agriculture/grants/lasa"],
    "document_urls": ["https://dem.ri.gov/sites/g/files/xkgbur861/files/2024-10/lasa-presentation-2025.pdf"]
  },
  {
    "grant_name": "NH Farm to School Local Food Incentive Pilot Program",
    "grant_description": "The NH Farm to School Local Food Incentive Pilot Program aims to increase the use of New Hampshire products in school meal programs by enhancing collaboration between NH schools and producers. It involves purchasing local, minimally processed foods for school breakfasts, lunches, or fresh fruit and vegetable programs. The program is designed to connect schools with producers and support the procurement process.",
    "website_urls": ["https://www.agriculture.nh.gov/divisions/agricultural-development/grant-program.htm"],
    "document_urls": ["https://www.agriculture.nh.gov/publications-forms/documents/rfa-2025-farmtoschool.pdf"]
  },
  {
    "grant_name": "Minnesota Transition to Organic Cost-Share Program",
    "grant_description": "This program supports Minnesota farmers transitioning to organic farming by reimbursing costs associated with working with an organic certifying agency during the transition period. It aims to enhance farmer confidence and success in becoming fully certified organic.",
    "website_urls": ["https://www.mda.state.mn.us/minnesota-transition-organic-cost-share-program"],
    "document_urls": ["https://www.mda.state.mn.us/sites/default/files/docs/2024-04/MNtransitionorganic2024application.pdf"]
  },
  {
    "grant_name": "Farmers Drought Relief Fund",
    "grant_description": "The Farmers Drought Relief Fund aims to assist Maine farmers in overcoming the adverse effects of drought by providing grants for developing agricultural water management plans and installing agricultural water sources. Projects should focus on sustainable irrigation for cropland.",
    "website_urls": ["https://www.maine.gov/dacf/ard/grants/farmers-drought-relief-program.shtml"],
    "document_urls": ["https://www.maine.gov/DACF/ard/grants/documents/fdrf-rfa-2025.pdf"]
  },
  {
    "grant_name": "Farm to Fork - Kentucky",
    "grant_description": "The Farm to Fork program in Kentucky aims to increase awareness and support for the local food movement by encouraging organizations to host dinners that showcase 100 percent local farms, farmers, producers, and Kentucky Proud products. These events highlight the benefits of farm-to-table initiatives while benefiting a local charity, promoting community engagement with locally sourced agricultural products.",
    "website_urls": ["https://www.kyagr.com/marketing/farm-to-fork.html"],
    "document_urls": ["https://www.kyagr.com/marketing/documents/KYP_Fork_BrandGuidelines.pdf"]
  },
  {
    "grant_name": "Equine Welfare Assistance",
    "grant_description": "The Equine Welfare Assistance Grant aims to enhance the well-being of Colorado's domestic equines by funding projects and programs that support safety net initiatives, adoption programs, education, and awareness related to equine welfare. Eligible projects include education, outreach, safety net programs to keep equines in their homes, community support, and adoption promotion.",
    "website_urls": ["https://ag.colorado.gov/press-release/equine-welfare-assistance-grant-accepting-applications"],
    "document_urls": [
      "https://docs.google.com/presentation/d/1UWl-RINuX5kuvI6c4ptLXlcHiPvAmKb5qq8MXaPegT8/edit?usp=sharing",
      "https://docs.google.com/document/d/16deB-mJ5oBpmt46yQDuAzdoSXgGHR1vy_oOKOH7nc4U/edit?usp=sharing"
    ]
  }
]


AVAILABLE_TAGS_NULL = [
  "agriculture",
  "aquaculture",
  "capacity-building",
  "capital",
  "climate",
  "community-benefit",
  "conservation",
  "cost-share",
  "dairy",
  "distribution",
  "drought",
  "education",
  "equipment",
  "equine",
  "equine-owners",
  "food-safety",
  "farmer",
  "farm-to-school",
  "grant",
  "infrastructure",
  "irrigation",
  "local-food",
  "local-government",
  "logistics",
  "marketing",
  "mixed-operations",
  "nonprofit",
  "nutrient-management",
  "operational",
  "organic-certification",
  "organic-transition",
  "outreach",
  "planning",
  "pilot",
  "producer-group",
  "procurement",
  "processing",
  "research",
  "resilience",
  "reimbursement",
  "rolling",
  "rural",
  "safety-net",
  "school",
  "seafood",
  "seafood-harvester",
  "soil",
  "supply-chain",
  "technical-assistance",
  "training",
  "value-added",
  "water",
  "water-storage",
  "working-capital",
  "row-crops",
  "vegetables",
  "fruit",
  "livestock",
  "competitive",
  "match-required",
  "public-entity-eligible",
  "individual-eligible",
  "rfa-open",
  "wi",
  "va",
  "ri",
  "nh",
  "mn",
  "me",
  "ky",
  "co",
  "cooperative",
  "for-profit",
  "university",
  "extension",
  "tribal",
  "veteran",
  "beginning-farmer",
  "underserved",
  "youth",
  "food-access",
  "nutrition",
  "workforce",
  "energy",
  "renewable-energy",
  "water-quality",
  "soil-health",
  "wildlife-habitat",
  "pasture",
  "grazing",
  "manure-management",
  "disaster-relief",
  "flood"
]

def serialize_grant(grant):
    """Convert MongoDB document to JSON-serializable format"""
    grant['_id'] = str(grant['_id'])
    return grant

def tag_grant_with_llm(grant_name, grant_description):
    """Use GROQ LLM to tag a grant based on its description"""
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Create a prompt for the LLM
    prompt = f"""You are a grant classification system. Given a grant name and description, select the most relevant tags from the following list:

Available tags: {', '.join(AVAILABLE_TAGS)}

Grant Name: {grant_name}
Grant Description: {grant_description}

Instructions:
- Select between 2 to 5 most relevant tags from the available tags list
- Only use tags from the provided list
- Return ONLY the tags as a comma-separated list, nothing else
- Do not include explanations or additional text

Tags:"""

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 100
    }
    
    try:
        print(f"Sending request to GROQ API for grant: {grant_name}")
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"GROQ API error: {response.status_code} - {response.text}")
            return []
        
        result = response.json()
        
        # Extract the tags from the response
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0]['message']['content'].strip()
            print("LLM Response", content)
            # Parse the comma-separated tags
            tags = [tag.strip() for tag in content.split(',')]
            
            # Filter to only include valid tags from our predefined list
            valid_tags = [tag for tag in tags if tag in AVAILABLE_TAGS]
            
            print(f"Generated tags: {valid_tags}")
            return valid_tags
        else:
            print("No choices in GROQ API response")
            return []
            
    except requests.exceptions.Timeout:
        print("GROQ API request timed out")
        return []
    except Exception as e:
        print(f"Error calling GROQ API: {str(e)}")
        return []






def process_single_grant(grant: dict) -> dict:
    """
    Takes a single grant object, assigns tags, 
    and returns the updated grant object.
    """
    
    if 'grant_name' not in grant or 'grant_description' not in grant:
        raise ValueError("Grant must have 'grant_name' and 'grant_description'")
    
    tags = tag_grant_with_llm(grant['grant_name'], grant['grant_description'])
    grant['tags'] = tags
    return grant





def process_and_store_grants(grants: list) -> list:
    """
    Takes a list of grants, tags each one, 
    stores them in DB, and returns the stored grants.
    """

    processed = []  
    for grant in grants:
        tagged_grant = process_single_grant(grant)
        processed.append(tagged_grant)

    if processed:
        grants_collection.insert_many(processed)

    return processed






@app.route('/api/grants', methods=['GET'])
def get_grants():
    """Retrieve all grants from the database"""
    try:
        grants = list(grants_collection.find())
        serialized_grants = [serialize_grant(grant) for grant in grants]
        return jsonify({'grants': serialized_grants}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/grants', methods=['POST'])
def add_grants():
    """Add new grant to the database with LLM-based tagging"""
    try:
        data = request.json
        
        if not data or 'grant' not in data:
            return jsonify({'error': 'Invalid request format. Expected {grant: [...]}'}), 400
        
        grant_to_add = data['grant']     
        
        if not isinstance(grant_to_add, dict):
            return jsonify({'error': 'Each grant must be an object'}), 40
        grant_to_add= process_single_grant(grant_to_add)
        
        print(f"Grant '{grant_to_add['grant_name']}' tagged with: {grant_to_add["tags"]}")
    
        if grant_to_add:
            result = grants_collection.insert_one(grant_to_add)
        
        all_grants = list(grants_collection.find())
        serialized_grants = [serialize_grant(grant) for grant in all_grants]
        
        return jsonify({
            'message': f'Successfully added  {grant_to_add["grant_name"]}',
            'grants': serialized_grants
        }), 201
        
    except Exception as e:
        print(f"Error in add_grants: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/grants/<grant_id>', methods=['DELETE'])
def delete_grant(grant_id):
    """Delete a specific grant"""
    try:
        result = grants_collection.delete_one({'_id': ObjectId(grant_id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Grant not found'}), 404
        
        all_grants = list(grants_collection.find())
        serialized_grants = [serialize_grant(grant) for grant in all_grants]
        
        return jsonify({
            'message': 'Grant deleted successfully',
            'grants': serialized_grants
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tags', methods=['GET'])
def get_available_tags():
    """Get list of available tags"""
    return jsonify({'tags': AVAILABLE_TAGS}), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify database connection"""
    try:
        client.admin.command('ping')
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'groq_api': 'configured' if GROQ_API_KEY else 'missing',
            'grants_count': grants_collection.count_documents({})
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)