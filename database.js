const {MongoClient} = require('mongodb');
require('dotenv').config();

async function main(){
    const uri = "mongodb+srv://vhomesgroup:vhomes2019@cluster0.rmikc.mongodb.net/VHomes?retryWrites=true&w=majority";
    const client = new MongoClient(uri);
    try {
        await client.connect();
        await  listDatabases(client);
    } catch (e) {
        console.error(e);
    } finally {
        await client.close();
    }
}

async function addUser(client){
  const uri = process.env.URI;
  const client = new MongoClient(uri);
  try {
      await client.connect();

  } catch (e) {
      console.error(e);
  } finally {
      await client.close();
  }
};

main().catch(console.error);
