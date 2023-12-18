const { MongoClient } = require('mongodb');


const mongoose = require("mongoose");
// const OCR = require('./../models/card');

let db = "0";

const mongoConnect = callback => {

    mongoose.connect("mongodb://localhost:27017")
        .then(() => {
            console.log("mongodb connected");

            // const collection = new mongoose.model("Collection1", LogInSchema);
            // collection.insertMany(data);
            db = "1";
            console.log("shld be connected");
            displayCard();

        })
        .catch((err) => {
            console.log("failed to connect");
            throw err;
        })

};


const availableUser = async (val1, val2) => {
    const User = mongoose.model('Collection1', LogInSchema);

    // async function findUser() {
    try {
        const result = await User.findOne({ email: toString(val1), password: toString(val2) });

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


const displayCard = () => {
    const cardSchema = new mongoose.Schema({
        vehicle: String,
        number_plate_img: String,
        number_plate: String,
        Violation: String
    });

    // Define the model
    // const Card = mongoose.model('OCRdb', cardSchema);
    // console.log(Card);
    // if (Card) {
    //     console.log("card found");
    // }

    // (async () => {
    //     try {
    //         const cards = await Card.find({});

    //         if (cards && cards.length > 0) {
    //             console.log('Card found');
    //             // Iterate through each card and log its data
    //             cards.forEach(card => {
    //                 console.log('Name:', card.name);
    //                 console.log('ID:', card.id);
    //                 console.log('---');
    //             });
    //         } else {
    //             console.log('No cards found');
    //         }

    //         // Close the MongoDB connection
    //         await mongoose.connection.close();
    //     } catch (error) {
    //         console.error('Error fetching data from collection:', error);
    //     }
    // })();







    // Connection URI
    const uri = 'mongodb://localhost:27017'; // Update with your MongoDB connection URI

    // Database name
    const dbName = 'ORCdb'; // Update with your database name

    // Create a new MongoClient
    const client = new MongoClient(uri);

    console.log("this shld be connected ....")

    // Connect to the MongoDB server
    client.connect(err => {
        if (err) {
            console.error('Error connecting to MongoDB:', err);
            return;
        }
        else {
            console.log("Not working .")
        }

        console.log('Connected to MongoDB');

        // Access the database  
        const db = client.db(dbName);

        // Access a specific collection
        const collection = db.collection('collection1'); // Update with your collection name

        // Perform a query (e.g., find all documents in the collection)
        collection.find({}).toArray((err, documents) => {
            if (err) {
                console.error('Error querying collection:', err);
                return;
            }

            console.log('Documents:', documents);

            // Close the connection
            client.close();
        });

    });









    // Card.find(() => {
    //     if (err) {
    //         console.error('Error fetching data from collection:', err);
    //         return;
    //     }

    //     console.log('Documents in collection:');
    //     console.log(cards);

    // })

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
    email: {
        type: String,
        required: true
    },
    password: {
        type: String,
        required: true
    }
});

// The traffic personals emails are stored in db as follows :

const data = [
    {
        email: "160421733090@mjcollege.ac.in",
        password: "Ayman090"
    },
    {
        email: "160421733082@mjcollege.ac.in",
        password: "Hisham090"
    },
    {
        email: "160421733083@mjcollege.ac.in",
        password: "Musaib090"
    },
    {
        email: "160421733066@mjcollege.ac.in",
        password: "Raniya090"
    },
    {
        email: "160421733063@mjcollege.ac.in",
        password: "Poorvi090"
    },
    {
        email: "160421733084@mjcollege.ac.in",
        password: "Shafaat090"
    }
]

// module.exports = collection;
module.exports.mongoConnect = mongoConnect;
module.exports.availableUser = availableUser;