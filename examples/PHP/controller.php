<!--
        'controller.php'
        
        Team: Steven Fan, Bailey Fokin, Srikar Kota
        
        Main Page for Project BayLLE-H
-->

<!DOCTYPE html>
<html lang="en"> <!--START HTML-->
    
    <head>
        <!-- specifiers to set page characteristics -->
        <meta http-equiv="Content-Type" content="text/html; charset=shift_jis">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

        <!-- icon and title in the page tag -->
        <link rel="icon" type="image/png" href="./assets/img/icon_60x60.png">
        <title>RoboController</title>

        <!-- Bootstrap core CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" 
        integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
        
        <!-- custom styles for this page -->
        <link href="./assets/css/main.css" rel="stylesheet">


    </head>
  
    <body><!--START BODY-->
        <!-- navbar at the top of the screen -->
        <nav class="navbar-dark sticky-top bg-dark p-0 shadow">
            <a class="navbar-brand" style = " font-weight: bold; color: rgb(255,255,255);" href="."><img style="img-fluid;width:50px" src="./assets/img/icon_60x60.png" >408i | Project BayLLE-H</a>
            
            <!-- this menu appears when the page is very narrow (phones) -->
            <button class="navbar-toggler position-absolute d-md-none collapsed" type="button" data-toggle="collapse" data-target="#sidebar" aria-controls="sidebar" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
        </nav> <!-- end navbar -->


                
        <!-- SIDEBAR---------------------------------------------------------------------------------------------->
        <nav id="sidebar" class="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse">
            <div class="sidebar-sticky pt-3">
                <!-- first grouping; holds all main pages -->
                <ul class="nav flex-column">
                    
                    <li class="nav-item">
                        <a class="header" style = "padding-left: 10px; font-weight: bold; color: rgb(255,255,255)">Main Pages</a>
                    </li>
                    
                    <li class="nav-item">
                        <a class="nav-link" href=".">
                            <span data-feather="layout"></span>
                            Home Page <span class="sr-only"></span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="./dashboard.php">
                            <span data-feather="codesandbox"></span>
                            Dashboard <span class="sr-only"></span>
                        </a>
                    </li>

                    <li class="nav-item">
                        <a class="nav-link" href="./about.php">
                            <span data-feather="users"></span>
                            About <span class="sr-only"></span> 
                        </a>
                    </li>
                </ul>
                
                <ul class="nav flex-column">
                    
                    <li class="nav-item">
                        <a class="header" style = "padding-left: 10px; font-weight: bold; color: rgb(255,255,255)">Robot Controller</a>
                    </li>
                    
                    <li class="nav-item">
                        <a class="nav-link active" href="./controller.php">
                            <span data-feather="activity"></span>
                            RoboController <span class="sr-only">(current)</span>
                        </a>
                    </li>
                </ul>
                
                <!-- Robot pages -->
                <ul class="nav flex-column mt-3 mb-2">
                    <li class="nav-item">
                        <a class="header" style = "padding-left: 10px; font-weight: bold; color: rgb(255,255,255)">Robot Pages</a>
                    </li>
                    
                    <li class="nav-item">
                        <a class="nav-link" href="./baymax.php">
                            <span data-feather="aperture"></span>
                            Baymax <span class="sr-only"></span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="./robo_nurse_h.php">
                            <span data-feather="slack"></span>
                            RoboNurse-H <span class="sr-only"></span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="./walle.php">
                            <span data-feather="chrome"></span>
                            WALLE <span class="sr-only"></span>
                        </a>
                    </li>
                </ul>                
                
            </div>
        </nav> 
        <!-- END SIDEBAR------------------------------------------------------------------------------------------>

        <!-- main panel, holds dashboard elements. This section is right of the sidbar and below the nav bar-->
        <main role="main" class="col-md-9 ml-sm-auto col-lg-10 px-md-4">
            <div class=" d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
                <h3><b>Remote Robot Controller</b></h3>
            </div>

            <form>
                <!-- DROPDOWN BAR Robot select-->
                <div class="row justify-content-center" style = "position: relative; top: -15px;">
                    <div class="jumbotron text-center pt-4 pb-4 mb-0" style="background-color:#fff;">
                        <h3>Target Robot</h3>
                            <select class="form-control-lg text-center"  id="select_target" style="width:300px; text-align:center; background-color:#fff">
                                <option value= "" disabled selected hidden>Select Robot</option>
                                <option value="baymax">Baymax</option>
                                <option value="robonurse">RoboNurse-H</option>
                                <option value="walle">WALLE</option>
                                <option value="all">all</option>
                                
                            </select>
                    </div> 
                        
                        
                    <!-- DROPDOWN BAR Physician select-->
                    <div class="row justify-content-center">
                        <div class="jumbotron text-center pt-4 pb-4 mb-0" style="background-color:#fff">
                            <h3>Command Select</h3>
                                <select class="form-control-lg text-center"  id="select_command" style="width:300px; text-align:center; background-color:#fff">
                                    <option value= "" disabled selected hidden>Select Command</option>
                                    <option value="0">Halt</option>
                                    <option value="1">Wander</option>
                                    <option value="3">dance</option>
                                    <option value="4">forward</option>
                                </select>
                        </div> 
                    </div>
                </div>
                
                <div class="row justify-content-center" style = "position: relative; top: -15px;">
                    <button type="button" onclick="send_command()">send command</button>
                </div>
                
            </form>
            <script>
            
                function send_command() {
                    var targ = document.getElementById("select_target");
                    targ = targ.options[targ.selectedIndex].value;
                    
                    var com = document.getElementById("select_command");
                    com = com.options[com.selectedIndex].value;
                    
                    ws = new WebSocket("wss://35cbc5645e74.ngrok.io");
                    
                    ws.onmessage = function(e){ console.log(e.data); };
                            ws.onopen = () => ws.send(JSON.stringify({
                                type: "command",
                                user: targ,
                                command: com
                            }));
                    
                }
                
            </script>

        </main> <!-- end main panel -->
            

    </body> <!--END BODY-->
    
    
</html>



<!-- jquery js library -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>

<!-- bootstrap js library -->
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" 
    integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>

<!-- feather icon js pack -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/feather-icons/4.24.1/feather.min.js"></script>

<!-- this page's specific js library for icons -->
<script src="./assets/js/main.js"></script>
        