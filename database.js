const {MongoClient} = require('mongodb');
require('dotenv').config();

async function addUser(){
  const uri = process.env.URI;
  const client = new MongoClient(uri, { useUnifiedTopology: true });
  let email = document.querySelector('#name').value;
  let password = document.querySelector('#password').value;
  console.log(email);
  try {
      await client.connect();
      const db = client.db("VHomes");
      let collection = db.collection('users');
      await collection.insertOne({email: email, password: password})
  } catch (e) {
      console.error(e);
  } finally {
      await client.close();
  }
};

addUser().catch(console.error);
