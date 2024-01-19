import copy
import json
import argparse

existing_query = {
    "query": {
        "type": "group",
        "logical_operator": "and",
        "nodes": [
            {
                "type": "group",
                "logical_operator": "and",
                "nodes": [
                    {
                        "type": "group",
                        "logical_operator": "and",
                        "nodes": [
                            {
                                "type": "terminal",
                                "service": "text",
                                "parameters": {
                                    "attribute": "rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession",
                                    "operator": "in",
                                    "negation": False,
                                    "value": ["UUUUUUU"]
                                }
                            },
                            {
                                "type": "terminal",
                                "service": "text",
                                "parameters": {
                                    "attribute": "rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_name",
                                    "operator": "exact_match",
                                    "value": "UniProt",
                                    "negation": False
                                }
                            }
                        ],
                        "label": "nested-attribute"
                    },
                    {
                        "type": "group",
                        "logical_operator": "and",
                        "nodes": [
                            {
                                "type": "terminal",
                                "service": "text",
                                "parameters": {
                                    "attribute": "rcsb_polymer_entity_annotation.annotation_id",
                                    "operator": "exact_match",
                                    "negation": False,
                                    "value": "PPPPPPP"
                                }
                            },
                            {
                                "type": "terminal",
                                "service": "text",
                                "parameters": {
                                    "attribute": "rcsb_polymer_entity_annotation.type",
                                    "operator": "exact_match",
                                    "value": "Pfam",
                                    "negation": False
                                }
                            }
                        ],
                        "label": "nested-attribute"
                    }
                ],
                "label": "text"
            },
            {
                "type": "group",
                "nodes": [
                    {
                        "type": "group",
                        "logical_operator": "and",
                        "nodes": [
                            {
                                "type": "terminal",
                                "service": "text_chem",
                                "parameters": {
                                    "attribute": "rcsb_chem_comp_related.resource_accession_code",
                                    "operator": "exact_match",
                                    "negation": False,
                                    "value": "DUMMYCHEMBL"
                                }
                            },
                            {
                                "type": "terminal",
                                "service": "text_chem",
                                "parameters": {
                                    "attribute": "rcsb_chem_comp_related.resource_name",
                                    "operator": "exact_match",
                                    "value": "ChEMBL",
                                    "negation": False
                                }
                            }
                        ],
                        "label": "nested-attribute"
                    }
                ],
                "logical_operator": "or"
            }
        ]
    },
    "return_type": "entry",
    "request_options": {
        "paginate": {
            "start": 0,
            "rows": 25
        },
        "results_content_type": [
            "experimental"
        ],
        "sort": [
            {
                "sort_by": "score",
                "direction": "desc"
            }
        ],
        "scoring_strategy": "combined"
    }
}
def add_values_to_query(existing_query,uniprot_id, pfam_id ,values_to_add):
    # Deep copy the existing query to avoid modifying the original
    new_query = copy.deepcopy(existing_query)
    
    #Asing the uniprot_id 
    new_query["query"]["nodes"][0]["nodes"][0]["nodes"][0]["parameters"]["value"][0] = uniprot_id
    new_query["query"]["nodes"][0]["nodes"][1]["nodes"][0]["parameters"]["value"] = pfam_id
    # Iterate over the values to add
    for value in values_to_add:
        # Create a new node for each value
        new_node = {
            "type": "group",
            "logical_operator": "and",
            "nodes": [
                {
                    "type": "group",
                    "logical_operator": "and",
                    "nodes": [
                        {
                            "type": "terminal",
                            "service": "text_chem",
                            "parameters": {
                                "attribute": "rcsb_chem_comp_related.resource_accession_code",
                                "operator": "exact_match",
                                "negation": False,
                                "value": value
                            }
                        },
                        {
                            "type": "terminal",
                            "service": "text_chem",
                            "parameters": {
                                "attribute": "rcsb_chem_comp_related.resource_name",
                                "operator": "exact_match",
                                "value": "ChEMBL",
                                "negation": False
                            }
                        }
                    ],
                    "label": "nested-attribute"
                }
            ],
            "logical_operator": "or"
        }

        # Add the new node to the existing query
        new_query["query"]["nodes"][1]["nodes"].append(new_node)

    return new_query

def main():
    # Argument parser
    parser = argparse.ArgumentParser(description="Add values to an existing query.")
    parser.add_argument("uniprot_id", help="UniProt identifier (e.g., P00918)")
    parser.add_argument("pfam_id", help="Pfam identifier (e.g., PF00194)")
    parser.add_argument("values_to_add", nargs="+", help="Values to add (e.g., CHEMBL578165 CHEMBL573209)")
    args = parser.parse_args()
    # Call the function to add values to the existing query
    updated_query = add_values_to_query(existing_query, args.uniprot_id, args.pfam_id ,args.values_to_add)


    # Print the updated query
    print(json.dumps(updated_query, indent=2))

if __name__ == "__main__":
    main()