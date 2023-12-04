const path = require('path');

const express = require('express');

// const adminController = require('../controllers/admin');

const router = express.Router();                         //basically , using this to route our stuff throu files.

sumPg = (req , res , next ) =>{
    res.render('sumpg');
}

router.get('/' , sumPg); 




let currentFrame = ''; 

router.get('/receive_frame', (req, res) => {
  console.log("running on rcv frame get");
    const { frame } = req.body;

    currentFrame = frame; 
    // res.redirect('/display_frames');
    console.log('Frame ');

    res.send(currentFrame);

  }
);


router.post('/receive_frame', (req, res) => {
    const { frame } = req.body;

    currentFrame = frame; // Update the current frame

    // console.log('Frame ');

    res.status(200).send("Frame received");



    // res.body =  {frame : frame} ;
    // console.log(res.body.frame);
    }
);

router.post('/send-frame' , (req , res , next) =>{
  // console.log("the data being sent to the ejs is :" , currentFrame);
  res.send(currentFrame);
})





router.get('/display_frames', (req, res) => {

    res.render('mainpg.ejs', {
      myFrame : currentFrame ,
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