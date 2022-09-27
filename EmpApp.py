<!DOCTYPE html>
<html lang="en">
   <head>
      <!-- basic -->
      <meta charset="utf-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <!-- mobile metas -->
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta name="viewport" content="initial-scale=1, maximum-scale=1">
      <!-- site metas -->
      <title>Add Employee Details</title>
      <meta name="keywords" content="">
      <meta name="description" content="">
      <meta name="author" content="">
      <!-- bootstrap css -->
      <link rel="stylesheet" href="css/bootstrap.min.css">
      <!-- style css -->
      <link rel="stylesheet" href="css/style.css">
      <!-- Responsive-->
      <link rel="stylesheet" href="css/responsive.css">
      <!-- fevicon -->
      <link rel="icon" href="images/fevicon.png" type="image/gif" />
      <!-- Scrollbar Custom CSS -->
      <link rel="stylesheet" href="css/jquery.mCustomScrollbar.min.css">
      <!-- Tweaks for older IEs-->
      <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css">
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/fancybox/2.1.5/jquery.fancybox.min.css" media="screen">
      <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script><![endif]-->
      <link rel="stylesheet" href="css/employeeLeave.css">
      <link rel="stylesheet" href="css/payroll.css">
   </head>




   <!-- body -->
   <body class="main-layout">
      <!-- loader  -->
      <div class="loader_bg">
         <!-- <div class="loader"><img src="images/loading.gif" alt="#" /></div> -->
      </div>
      <!-- end loader -->
      <div id="mySidepanel" class="sidepanel">
         <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">×</a>
         <form action="/addemp" autocomplete="on" method = "POST" enctype="multipart/form-data">
            <a href="index.html">Home </a>
         <a href="about.html">About</a>
         <button type="submit" style="background: black; height: 45px; width: 200px; color:white; font:oblique;" formaction="http://3.134.115.108:80/">Add Employee</button>
         <button type="submit" style="background: black; height: 45px; width: 200px; color:white; font:oblique;" formaction="http://3.134.115.108:80/find">Find Employee</button>
         <button type="submit" style="background: black; height: 45px; width: 200px; color:white; font:oblique;" formaction="http://3.134.115.108:80/empLeave">Apply Leave</button>
         <button type="submit" style="background: black; height: 45px; width: 200px; color:white; font:oblique;" formaction="http://3.134.115.108:80/empPayroll">Payroll</button>
         </form>
      </div>

      <!-- header -->
      <header>
         <!-- header inner -->
         <div class="header">
            <div class="container-fluid">
               <div class="row">
                  <div class="col-md-4 col-sm-4">
                     <div class="logo">
                        <!-- <a href="index.html"><img src="images/logo.png" alt="#" /></a> -->
                     </div>
                  </div>
                  <div class="col-md-8 col-sm-8">
                     <div class="right_bottun">
                        <ul class="conat_info d_none ">
                           <li><a href="#"><i class="fa fa-user" aria-hidden="true"></i></a></li>
                           <li><a href="#"><i class="fa fa-search" aria-hidden="true"></i></a></li>
                        </ul>
                        <button class="openbtn" onclick="openNav()"><img src="images/menu_icon.png" alt="#"/> </button> 
                     </div>
                  </div>
               </div>
            </div>
         </div>
      </header>
      <!-- end header inner -->
      <!-- end header -->
      
      <!-- banner -->
      <section class="banner_main">
         <center>
            <font color="black" size="4" style="font-family: avenir">
         
               <h1 style="color: DodgerBlue">Employee Database</h1>
        <form action="/addemp" autocomplete="on" method = "POST" enctype="multipart/form-data">

            <button type="submit" formaction="/getemp" style="background: grey; height: 45px; width: 300px; color:white; font:oblique;">GET EMPLOYEE INFORMATION</button><br><br>

              Employee ID:<br> <input style="height:25px;font-size:14pt; color:grey;" type="number" name="emp_id" autofocus size="40"><br><br>

              First Name:<br> <input style="height:25px;font-size:14pt;color:grey;" type="text" name="first_name" ><br><br>

              Last Name:<br> <input style="height:25px;font-size:14pt;color:grey;" type="text" name="last_name"><br><br>

              Primary Skills:<br> <input style="height:25px;font-size:14pt;color:grey;" type="text" name="pri_skill"><br><br>

              Location:<br> <input style="height:25px;font-size:14pt;color:grey;" type="text" name="location"><br><br>

              Salary:<br> <input style="height:25px;font-size:14pt;color:grey;" type="text" name="salary"><br><br>

              Image: <input type=file name="emp_image_file" style="height:40px;font-size:14pt;color:grey;"> <br><br>

              <button type="submit" style="background: grey; height: 45px; width: 200px; color: white; size: 5; font:oblique;">UPDATE DATABASE</button>

        </form>
      </font>
   </center>
      </section>
      <!-- end banner -->

      




      <!--  footer -->
      <footer>
         <div class="footer bottom_cross1">
            <div class="container">
               <div class="row">
                  <div class="col-md-4">
                     <ul class="location_icon">
                        <li><a href="#"><i class="fa fa-map-marker" aria-hidden="true"></i></a> Address : Lorem Ipsum <br> is simply dummy 
                        </li>
                        <li><a href="#"><i class="fa fa-phone" aria-hidden="true"></i></a>Phone :  +(1234) 567 890</li>
                        <li><a href="#"><i class="fa fa-envelope" aria-hidden="true"></i></a>Email : demo@gmail.com</li>
                     </ul>
                     <form class="bottom_form">
                        <h3>Newsletter</h3>
                        <input class="enter" placeholder="Enter your email" type="text" name="Enter your email">
                        <button class="sub_btn">subscribe</button>
                     </form>
                  </div>
                  <div class="col-md-8">
                     <div class="map">
                        <figure><img src="images/map.png" alt="#"/></figure>
                     </div>
                  </div>
               </div>
            </div>
            <div class="copyright">
               <div class="container">
                  <div class="row">
                     <div class="col-md-12">
                        <p>© 2019 All Rights Reserved. Design by<a href="https://html.design/"> Free Html Templates</a></p>
                     </div>
                  </div>
               </div>
            </div>
         </div>
      </footer>
      <!-- end footer -->




      
      <!-- Javascript files-->
      <script src="js/jquery.min.js"></script>
      <script src="js/popper.min.js"></script>
      <script src="js/bootstrap.bundle.min.js"></script>
      <script src="js/jquery-3.0.0.min.js"></script>
      <!-- sidebar -->
      <script src="js/jquery.mCustomScrollbar.concat.min.js"></script>
      <script src="js/custom.js"></script>
      <script>
         function openNav() {
           document.getElementById("mySidepanel").style.width = "250px";
         }
         
         function closeNav() {
           document.getElementById("mySidepanel").style.width = "0";
         }
      </script>
   </body>
</html>
