
# Vending Machine

Vending Mahcine Tracking Application to manage all the vending machine in MUIC using Flask framework.

## Installation

1.Initialize and activate virtual environment

```
python3 -m venv venv
source venv/bin/activate
```
2.Install flask and sqlalchemy
```
pip install Flask
pip install flask-sqlalchemy
```
3.Run the project
```
flask run
```




## Machine APIs

### POST ```/api/machine/create```

Method to create the vending machine.

| Request Field | Field Type    | Description                     | Optional |
| :---         | :---         | :---                           | :---    |
| name          | String        | Name of the vending machine     | False    |
| address          | String     | Address of the vending machine. | False    |

**Sample Response  ```200 Ok```**
```
Added a new machine to the database!
```
**Possible Error**

| Error Code | Description   |
| :---         | :---        |
| 500 Internal Server Error  | Something went wrong when adding data to the database.  |

### GET ```/api/machine/get/<id>```

Method to get the vending machine with its stock by id.

**Sample Response  ```200 Ok```**

```json
{
    "address": "IC Bld. Canteen Floor.2",
    "id": 1,
    "name": "Machine 1",
    "stock": [
        {
            "id": 1,
            "machine_id": 1,
            "name": "Pringle",
            "price": 20,
            "quantity": 15,
            "type": "Snack"
        },
        {
            "id": 2,
            "machine_id": 1,
            "name": "Coke",
            "price": 20,
            "quantity": 6,
            "type": "Beverage"
        },
        {
            "id": 3,
            "machine_id": 1,
            "name": "Sprite",
            "price": 20,
            "quantity": 10,
            "type": "Beverage"
        }
    ]
}

```
**Possible Error**

| Error Code | Description   |
| :---         | :---        |
| 404 Not Found  | Can’t find the machine with the id given in the database.|
| 500 Internal Server Error | Something went wrong when getting data from the database.|

### GET ```/api/machine/get```

Method to get all the vending machines with its stock.

**Sample Response  ```200 Ok```**
```json
{
    "machines": [
        {
            "address": "IC Bld. Canteen Floor.2",
            "id": 1,
            "name": "Machine 1",
            "stock": [
                {
                    "id": 1,
                    "machine_id": 1,
                    "name": "Pringle",
                    "price": 20,
                    "quantity": 15,
                    "type": "Snack"
                },
                {
                    "id": 2,
                    "machine_id": 1,
                    "name": "Coke",
                    "price": 20,
                    "quantity": 6,
                    "type": "Beverage"
                },
                {
                    "id": 3,
                    "machine_id": 1,
                    "name": "Sprite",
                    "price": 20,
                    "quantity": 10,
                    "type": "Beverage"
                }
            ]
        },
        {
            "address": "Aditayathorn Bld. Canteen G.Floor",
            "id": 2,
            "name": "Machine 2",
            "stock": [
                {
                    "id": 4,
                    "machine_id": 2,
                    "name": "Haribo",
                    "price": 10,
                    "quantity": 4,
                    "type": "Snack"
                },
                {
                    "id": 5,
                    "machine_id": 2,
                    "name": "Ichitan Lemon",
                    "price": 20,
                    "quantity": 15,
                    "type": "Beverage"
                }
            ]
        }
    ]
}
```

| Error Code | Description   |
| :---         | :---        |
| 500 Internal Server Error  | Something went wrong when getting data to the database.  |


### PUT ```/api/machine/update/<id>```

Method to update the name or address of the vending machine.

| Request Field | Field Type    | Description                     | Optional |
| :---         | :---         | :---                           | :---    |
| name          | String        | Name of the vending machine     | True    |
| address          | String     | Address of the vending machine. | True    |

**Sample Response  ```200 Ok```**
```
Updated the vending machine information!
```
**Possible Error**

| Error Code | Description   |
| :---         | :---        |
| 404 Not Found  | Can’t find the machine with the id given in the database.|
| 500 Internal Server Error  | Something went wrong while updating machine information. |

### DELETE ```/api/machine/delete/<id>```

Method to delete the vending machine by id.

**Sample Response  ```200 Ok```**
```
Delete machine successfully!
```
| Error Code | Description   |
| :---         | :---        |
| 404 Not Found  | Can’t find the machine with the id given in the database.|
| 500 Internal Server Error  | Something went wrong while deleting machine from the database. |








## Product APIs

### POST ```/api/product/create```

Method to add the product to the vending machine.

| Request Field | Field Type   | Description                     | Optional |
| :---         | :---          | :---                           | :---    |
| name          | String       | Name of the product   | False    |
| price          | Integer     | Price of the product | False    |
| type          | String     | Type of the product | False    |
| machine_id          | Integer       | ID of the machine that you want to assign the product to. | False    |
| quantity          | Integer       | Number of products you want to add to the machine. | False    |


**Sample Response  ```200 Ok```**
```
Added a new product to the database!
```
**Possible Error**

| Error Code | Description   |
| :---         | :---        |
| 500 Internal Server Error  | Something went wrong when adding data to the database.  |

### GET ```/api/product/get/<id>```

Method to get a product by id.

**Sample Response  ```200 Ok```**
```json
{
    "id": 1,
    "machine_id": 1,
    "name": "Pringle",
    "price": 20,
    "quantity": 15,
    "type": "Snack"
}
```
| Error Code | Description   |
| :---         | :---        |
| 404 Not Found  | Can’t find the product with the id given in the database.|
| 500 Internal Server Error  | Something went wrong when getting data from the database. |


### GET ```/api/product/get```

Method to get all the products.

**Sample Response  ```200 Ok```**
```json
[
    {
        "id": 1,
        "machine_id": 1,
        "name": "Pringle",
        "price": 20,
        "quantity": 15,
        "type": "Snack"
    },
    {
        "id": 2,
        "machine_id": 1,
        "name": "Coke",
        "price": 20,
        "quantity": 6,
        "type": "Beverage"
    },
    {
        "id": 3,
        "machine_id": 1,
        "name": "Sprite",
        "price": 20,
        "quantity": 10,
        "type": "Beverage"
    },
    {
        "id": 4,
        "machine_id": 2,
        "name": "Haribo",
        "price": 10,
        "quantity": 4,
        "type": "Snack"
    },
    {
        "id": 5,
        "machine_id": 2,
        "name": "Ichitan Lemon",
        "price": 20,
        "quantity": 15,
        "type": "Beverage"
    }
]
```
**Possible Error**

| Error Code | Description   |
| :---         | :---        |
| 500 Internal Server Error  | Something went wrong when getting data from the database. |


### PUT ```/api/product/update/<id>```

Method to update the information of the product based on id of the product.

| Request Field | Field Type   | Description                     | Optional |
| :---         | :---          | :---                           | :---    |
| name          | String       | New name of the product  | True    |
| price          | Integer     | New price of the product | True    |
| type          | String     | New type of the product | True   |
|quantity        | Integer     | New quantity| True   |

**Sample Response  ```200 Ok```**

```
Updated the product information!
```

**Possible Error**

| Error Code | Description   |
| :---         | :---        |
| 400 Bad Request | The quantity has to be >= 1 |
| 404 Not Found  | Can’t find the product with the id given in the database.|
| 500 Internal Server Error | Something went wrong when updating data to the database. |

### DELETE ```/api/product/delete/<id>```
Method to delete the product from the vending machine.

| Request Field | Field Type   | Description                     | Optional |
| :---         | :---          | :---                           | :---    |
| name          | String       | Name of the product you want to delete | False    |
| machine_id          | Integer     | ID of the machine you want to delete the product from | False   |
| quantity          | Integer     | Number of products you want to delete | False|

**Sample Response  ```200 Ok```**
```
Delete product from stock!
```
| Error Code | Description   |
| :---         | :---        |
| 404 Not Found  | Can’t find the product with the id given in the database.|
| 500 Internal Server Error  | Something went wrong when deleting data from the database. |
