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
        "JobImportationInfo" : {
            "type": "object",
            "properties": {
                "job_id": { "type" : "string"},
                "job_name": { "type" : "string"},
                "product": { "type" : "string"},
                "year": { "type" : "number"}
            }
        },
        "JobImportationResponse" : {
            "type": "object",
            "properties": {
                "status": { "type" : "string"},
                "message": { "type" : "string"},
                'jobs': {
                        'type': 'array',
                        '$ref': '#/components/schemas/JobImportationInfo'
                    },
            }
        },
        "Processing" : {
            "type": "object",
            "properties": {
                "_id": { "type" : "string"},
                "cultivation": { "type" : "string"},
                "type": { "type" : "string"},
                "year": { "type" : "number"},
                "quantity": { "type" : "number"}
            }
        },
        "NewProcessing" : {
            "type": "object",
            "properties": {
                "cultivation": { "type" : "string"},
                "type": { "type" : "string"},
                "year": { "type" : "number"},
                "quantity": { "type" : "number"}
            }
        },
        "JobProcessingInfo" : {
            "type": "object",
            "properties": {
                "job_id": { "type" : "string"},
                "job_name": { "type" : "string"},
                "classification": { "type" : "string"},
                "year": { "type" : "number"}
            }
        },
        "JobProcessingResponse" : {
            "type": "object",
            "properties": {
                "status": { "type" : "string"},
                "message": { "type" : "string"},
                'jobs': {
                        'type': 'array',
                        '$ref': '#/components/schemas/JobProcessingInfo'
                    },
            }
        }
    }