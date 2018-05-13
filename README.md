# Station Service API Documentation


* [Request & Response Examples](#request--response-examples)


## Request & Response Examples

### API Resources

  - [GET /stations](#get_all_stations)
  - [GET /station/[id]](#get_station)
  - [POST /station](#create_station)
  - [PUT /station](#update_station)
  - [DELETE /station/public_id](#delete_station)

### GET /stations

Example: http://172.104.135.186:5000/stations

Response body:

    [
      {
        id: 2,
        lang: 37.015,
        latd: 39.7505,
        name: "Sivas",
        public_id: "c9efdf46-4bdd-4cc2-a2f5-65c48261c445",
      },
      {
        id: 3,
        lang: 32.8128,
        latd: 39.9179,
        name: "Ankara",
        public_id: "7e5c096a-4cc8-419b-940c-064677e873d7",
      },
    ]

### GET /station/id

Example: http://172.104.135.186:5000/station/2

Response body:

    {
        id: 2,
        lang: 37.015,
        latd: 39.7505,
        name: "Sivas",
        public_id: "c9efdf46-4bdd-4cc2-a2f5-65c48261c445",
    }
    
### POST /station

Example: http://172.104.135.186:5000/station

Request body:

    [
        {
          name: "Sivas_Update"
          lang: 37.015,
          latd: 39.7505
        }
    ]
    
Response body:

  {
        id: 2,
        lang: 37.015,
        latd: 39.7505,
        name: "Sivas",
        public_id: "c9efdf46-4bdd-4cc2-a2f5-65c48261c445",
    }

### PUT /station

Example: http://172.104.135.186:5000/station

Request body:

    [
        {
          id: 2,
          name: "Sivas_Update"
          lang: 37.015,
          latd: 39.7505
        }
    ]
    
Response body:

  {message: 'Station has updated!}
 
### DELETE /station/public_id

Example: http://172.104.135.186:5000/station/c9efdf46-4bdd-4cc2-a2f5-65c48261c445

Response body:

  {message: 'Station has deleted!'}
