const mongoose=require("mongoose");

let db = "0" ;

const mongoConnect = callback =>{  

    mongoose.connect("mongodb+srv://mohammedaymanquadri:Ayman2004@cluster1.zy5lsnn.mongodb.net/")
    .then(() => {
    console.log("mongodb connected");

    // const collection = new mongoose.model("Collection1" , LogInSchema);
    // collection.insertMany(data);
    db = "1" ;
    console.log("shld be connected");

    })
    .catch((err) => {
    console.log("failed to connect");
    throw err ;
    })

};


const availableUser = (val1 , val2) =>{
    const User = mongoose.model('Collection1', LogInSchema);

    // async function findUser() {
        try {
          const result = User.findOne({ email : toString(val1) , password : toString(val2) });
      
          if (result) {
            console.log(`Found a matching document: ${result}`);
            return true;
            // Do something with the matching document
          } else {
            console.log('No document found matching the search string.');
            return false;
          }
        } catch (err) {
          console.error('Error occurred:', err);
          // Handle the error
        }
    //   }
      
    //findUser();
}



// async function addUser() {
//     try {
//       // Connect to the MongoDB server
//       await client.connect();
  
//       // Access your database
//       const db1 = client.db(dbName);
  
//       // Create a user with desired privileges
//       await db1.createUser({
//         user: 'new_user',
//         pwd: 'password123',
//         roles: [{ role: 'readWrite', db: dbName }]
//       });
  
//       console.log('User created successfully');
//     } catch (error) {
//       console.error('Error creating user:', error);
//     } finally {
//       // Close the connection
//       await client.close();
//     }
//   }
  
// addUser();



const LogInSchema = new mongoose.Schema({
    email:{
        type: String,
        required : true
    },
    password:{
        type: String,
        required : true
    }
});

// The traffic personals emails are stored in db as follows :

const data = [
    {
        email : "160421733090@mjcollege.ac.in",
        password : "Ayman090"
    },
    {
        email : "160421733082@mjcollege.ac.in",
        password : "Hisham090"
    },
    {
        email : "160421733083@mjcollege.ac.in",
        password : "Musaib090"
    },
    {
        email : "160421733066@mjcollege.ac.in",
        password : "Raniya090"
    },
    {
        email : "160421733063@mjcollege.ac.in",
        password : "Poorvi090"
    },
    {
        email : "160421733084@mjcollege.ac.in",
        password : "Shafaat090"
    }
]

// module.exports = collection;
module.exports.mongoConnect = mongoConnect;
module.exports.availableUser = availableUser;