from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mysql.connector import connection
from common import logger

DEFAULT_CREDIT_LIMIT = 2000

app = FastAPI()

def create_connection():
    return connection.MySQLConnection(
        host='127.0.0.1',
        user='santhosh',
        password='pavan',
        database='paylater'
    )

def to_json(cursor):
    columns = [column[0] for column in cursor.description]
    
    response_json = []
    for row in cursor.fetchall():
        data = dict(zip(columns, row))
        response_json.append(data)
    return response_json

class UserCreate(BaseModel):
    name: str
    email: str
    balance: int

class MerchantCreate(BaseModel):
    name: str
    email: str
    fee: int

class TransactionCreate(BaseModel):
    u_id: int
    m_id: int
    amount: int

@app.post("/newUser")
async def new_user(user: UserCreate):
    response_msg = {
        "status" : "success",
        "data" : None,
        "message" : None
    }
    try:
        conn = create_connection()
        cursor = conn.cursor()
        query = f"INSERT INTO user (name, email, balance) VALUES ('{user.name}', '{user.email}', {user.balance})"
        cursor.execute(query)
        conn.commit()

        msg = "User add Successfully!"
        logger.info(msg)
        response_msg["message"] = msg
    except Exception as ex:
        response_msg["status"] = "failed"
        response_msg["message"] = str(ex)
        logger.error(response_msg["message"])
    finally:
        cursor.close()
        conn.close()
    return response_msg

@app.post("/newMerchant")
def new_merchant(merchant: MerchantCreate):
    response_msg = {
        "status": "success",
        "data": None,
        "message": None
    }

    try:
        conn = create_connection()
        cursor = conn.cursor()
        query = f"INSERT INTO merchant (name, email, fee) VALUES ('{merchant.name}', '{merchant.email}', {merchant.fee})"
        cursor.execute(query)
        conn.commit()

        msg = "Merchant added Successfully!"
        logger.info(msg)
        response_msg["message"] = msg
    except Exception as ex:
        response_msg["status"] = "failed"
        response_msg["message"] = str(ex)
        logger.error(response_msg["message"])
    finally:
        cursor.close()
        conn.close()
    return response_msg

@app.post("/transact")
async def transact(transaction: TransactionCreate):
    response_msg = {
        "status": "success",
        "data": None,
        "message": None
    }

    try:
        conn = create_connection()
        cursor = conn.cursor(buffered=True)

        query = f"INSERT INTO transactions (u_id, m_id, amount) VALUES ({transaction.u_id}, {transaction.m_id}, {transaction.amount})"
        cursor.execute(query)
        conn.commit()

        query = f"SELECT balance FROM user WHERE user_id={transaction.u_id}"
        cursor.execute(query)
        balance = float(cursor.fetchone()[0])

        if balance >= transaction.amount:
            query = f"UPDATE user SET balance={balance - transaction.amount} WHERE user_id={transaction.u_id}"
            cursor.execute(query)
            conn.commit()
            response = {"message": "Transaction successfully updated!"}
        else:
            response = {"error": "Insufficient balance"}
    except Exception as ex:
        response_msg["status"] = "failed"
        response_msg["message"] = str(ex)
    finally:
        cursor.close()
        conn.close()
    return response_msg


@app.get("/getMerchant/{mid}")
async def get_merchant(mid: int):
    response_msg = {
        "status": "success",
        "data": None,
        "message": None
    }

    try:
        conn = create_connection()
        cursor = conn.cursor(buffered=True)
        cursor.execute(f"SELECT * FROM merchant WHERE merchant_id={mid}")
        response_json = to_json(cursor)
        response_msg["data"] = response_json

        msg = "Merchant retrieved successfully"
        logger.info(msg)
        response_msg["message"] = msg
    except Exception as ex:
        response_msg["status"] = "failed"
        response_msg["message"] = str(ex)
        logger.error(response_msg["message"])
    finally:
        cursor.close()
        conn.close()

    return response_msg

@app.post("/updateFee")
async def update_fee(mid: int, fee: int):
    response_msg = {
        "status": "success",
        "data": None,
        "message": None
    }

    try:
        conn = create_connection()
        cursor = conn.cursor()
        query = f"UPDATE merchant SET fee={fee} WHERE merchant_id={mid}"
        cursor.execute(query)
        conn.commit()

        msg = "Merchant fee updated successfully"
        logger.info(msg)
        response_msg["message"] = msg
    except Exception as ex:
        response_msg["status"] = "failed"
        response_msg["message"] = str(ex)
        logger.error(response_msg["message"])
    finally:
        cursor.close()
        conn.close()

    return response_msg

@app.post("/repay")
async def repay(name: str, amount: int):
    response_msg = {
        "status": "success",
        "data": None,
        "message": None
    }

    try:
        conn = create_connection()
        cursor = conn.cursor()
        query = f"SELECT balance FROM user WHERE name='{name}'"
        cursor.execute(query)
        balance = float(cursor.fetchone()[0])

        query = f"UPDATE user SET balance={balance + amount} WHERE name='{name}'"
        cursor.execute(query)
        conn.commit()

        msg = "Repayment successful"
        logger.info(msg)
        response_msg["message"] = msg
    except Exception as ex:
        response_msg["status"] = "failed"
        response_msg["message"] = str(ex)
        logger.error(response_msg["message"])
    finally:
        cursor.close()
        conn.close()

    return response_msg

@app.get("/fee/{merchant}")
async def get_merchant_fee(merchant: str):
    response_msg = {
        "status": "success",
        "data": None,
        "message": None
    }

    try:
        conn = create_connection()
        cursor = conn.cursor()
        query = f"SELECT fee FROM merchant WHERE name='{merchant}'"
        cursor.execute(query)
        fee = float(cursor.fetchone()[0])
        msg = "Merchant fee retrieved successfully"
        logger.info(msg)
        response_msg["data"] = {"fee": fee}
        response_msg["message"] = msg
    except Exception as ex:
        response_msg["status"] = "failed"
        response_msg["message"] = str(ex)
        logger.error(response_msg["message"])
    finally:
        cursor.close()
        conn.close()


    return response_msg

@app.get("/dues/{user}")
async def get_user_dues(user: str):
    response_msg = {
        "status": "success",
        "data": None,
        "message": None
    }

    try:
        conn = create_connection()
        cursor = conn.cursor()
        query = f"SELECT SUM(amount) FROM transactions WHERE u_id=(SELECT user_id FROM user WHERE name='{user}')"
        cursor.execute(query)
        dues = float(cursor.fetchone()[0])
        response_msg["data"] = {"dues": dues}

        msg = "User dues retrieved successfully"
        logger.info(msg)
        response_msg["message"] = msg
    except Exception as ex:
        response_msg["status"] = "failed"
        response_msg["message"] = str(ex)
        logger.error(response_msg["message"])
    finally:
        cursor.close()
        conn.close()


    return response_msg

@app.get("/usersAtLimit")
async def get_users_at_limit():
    response_msg = {
        "status": "success",
        "data": None,
        "message": None
    }

    try:
        conn = create_connection()
        cursor = conn.cursor()
        query = f"SELECT name FROM user WHERE balance={DEFAULT_CREDIT_LIMIT}"
        cursor.execute(query)
        users = [row[0] for row in cursor.fetchall()]
        response_msg["data"] = {"users": users}

        msg = "Users at credit limit retrieved successfully"
        logger.error(msg)
        response_msg["message"] = msg
    except Exception as ex:
        response_msg["status"] = "failed"
        response_msg["message"] = str(ex)
        logger.error(response_msg["message"])
    finally:
        cursor.close()
        conn.close()


    return response_msg

@app.get("/totalDues")
async def get_total_dues():
    response_msg = {
        "status": "success",
        "data": None,
        "message": None
    }

    try:
        conn = create_connection()
        cursor = conn.cursor()
        query = "SELECT SUM(amount) FROM transactions"
        cursor.execute(query)
        total_dues = float(cursor.fetchone()[0])
        response_msg["data"] = {"total_dues": total_dues}
        
        msg = "Total dues retrieved successfully"
        logger.info(msg)
        response_msg["message"] = msg
    except Exception as ex:
        response_msg["status"] = "failed"
        response_msg["message"] = str(ex)
        logger.error(response_msg["message"])

    return response_msg

