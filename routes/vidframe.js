const path = require('path');

const express = require('express');

const availableUser = require('./../Database/mongoose').availableUser;
// const adminController = require('../controllers/admin');

const router = express.Router();                         //basically , using this to route our stuff throu files.

sumPg = (req , res , next ) =>{
    res.render('sumpg');
}

router.get('/sum' , sumPg); 


router.post('/login' , (req, res, next) =>{
  // res.sendFile(path.join(__dirname, 'public', 'contact.html'));
  // res.render('contact');
  const email_value = req.body.email ;
  const pswd_value = req.body.password ;
  // console.log(email_value);
  if (availableUser(email_value , pswd_value)){
    console.log("correct user");
    res.render('index');
  };
  


})

router.get('/login' , (req, res, next) =>{
  res.render('contact');
});


let currentFrame1  = ''; 
let currentFrame2  = ''; 
let currentFrame3  = ''; 

router.get('/receive_frame1', (req, res) => {
  console.log("running on rcv frame get");
    const { frame } = req.body;

    currentFrame1 = frame; 
    // res.redirect('/display_frames');
    console.log('Frame ');

    res.send(currentFrame1);

  }
);


router.post('/receive_frame1', (req, res) => {
    const { frame } = req.body;

    currentFrame1 = frame; // Update the current frame

    // console.log('Frame ');

    res.status(200).send("Frame received at 1");

    }
);

// --------------------required code --------------------------------//

// router.post('/receive_frame2', (req, res) => {
//   const { frame } = req.body;

//   currentFrame2 = frame; // Update the current frame

//   // console.log('Frame ');

//   res.status(200).send("Frame received at 2");

//   }
// );

// router.post('/receive_frame3', (req, res) => {
//   const { frame } = req.body;

//   currentFrame3 = frame; // Update the current frame

//   // console.log('Frame ');

//   res.status(200).send("Frame received at 3");

//   }
// );

// --------------------                --------------------------------//



router.post('/send-frame1' , (req , res , next) =>{
  // console.log("the data being sent to the ejs is :" , currentFrame);
  res.send(currentFrame1);
})

// --------------------required code --------------------------------//


// router.post('/send-frame2' , (req , res , next) =>{
//   res.send(currentFrame2);
// })
// router.post('/send-frame3' , (req , res , next) =>{
//   res.send(currentFrame3);
// })

// --------------------                --------------------------------//




router.get('/display_frames1', (req, res) => {

    res.render('mainpg.ejs', {
      myFrame : currentFrame1 ,
    });
    
    // setTimeout(() => {
    //   res.redirect('/receive_frame');
    // }, 3000);

  });


router.get('/display_frames2', (req, res) => {

    res.render('mainpg2.ejs', {
      myFrame : currentFrame2 ,
    });
    
    // setTimeout(() => {
    //   res.redirect('/receive_frame');
    // }, 3000);

  });

router.get('/display_frames3', (req, res) => {

    res.render('mainpg3.ejs', {
      myFrame : currentFrame3 ,
    });
    
    // setTimeout(() => {
    //   res.redirect('/receive_frame');
    // }, 3000);

  });




  

// router.post('/display_frames', (req, res) => {
//   console.log("running");
// });

router.post('/delete_frame', (req, res) => {
  console.log("running");
    
  
    res.redirect('/receive_frame');
  });


module.exports = router;