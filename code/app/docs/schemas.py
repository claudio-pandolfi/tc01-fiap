def get_schemas():
    return {
        "Msg" : {
            "type": "object",
            "properties": {
                "msg": { "type" : "string"}
            }
        },
        "Message" : {
            "type": "object",
            "properties": {
                "status": { "type" : "string"},
                "message": { "type" : "string"}
            }
        },
        "Login" : {
            "type": "object",
            "properties": {
                "status": { "type" : "number"},
                "access_token": { "type" : "string"}
            }
        },
        "Exportation" : {
            "type": "object",
            "properties": {
                "_id": { "type" : "string"},
                "country": { "type" : "string"},
                "product": { "type" : "string"},
                "year": { "type" : "number"},
                "quantity": { "type" : "number"},
                "amount": { "type" : "number"}
            }
        },
        "NewExportation" : {
            "type": "object",
            "properties": {
                "country": { "type" : "string"},
                "product": { "type" : "string"},
                "year": { "type" : "number"},
                "quantity": { "type" : "number"},
                "amount": { "type" : "number"}
            }
        },
        "Importation" : {
            "type": "object",
            "properties": {
                "_id": { "type" : "string"},
                "country": { "type" : "string"},
                "product": { "type" : "string"},
                "year": { "type" : "number"},
                "quantity": { "type" : "number"},
                "amount": { "type" : "number"}
            }
        },
        "NewImportation" : {
            "type": "object",
            "properties": {
                "country": { "type" : "string"},
                "product": { "type" : "string"},
                "year": { "type" : "number"},
                "quantity": { "type" : "number"},
                "amount": { "type" : "number"}
            }
        },
        "JobExportationInfo" : {
            "type": "object",
            "properties": {
                "job_id": { "type" : "string"},
                "job_name": { "type" : "string"},
                "product": { "type" : "string"},
                "year": { "type" : "number"}
            }
        },
        "JobExportationResponse" : {
            "type": "object",
            "properties": {
                "status": { "type" : "string"},
                "message": { "type" : "string"},
                'jobs': {
                        'type': 'array',
                        '$ref': '#/components/schemas/JobExportationInfo'
                    },
            }
        }
    }