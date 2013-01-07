<head>
    <style type="text/css">
        #container_3d{
            position:relative;
        }
        .img_layer{
            position:absolute;
        }
    </style>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script src="./obj.js"></script>
    <script type="text/javascript">
        var position = 0
        var min_position = 0
        var max_position = 0
        $(document).ready(function(){
            for(var i=0; i<layers.length; i++){
                var layer = layers[i]
                var img = '<img id="img_'+i+'" class="img_layer" src="obj_'+layer.toString()+'.0.png" />';
                $("#container_3d").append(img);
                left = Math.round(layer);
                $("#img_"+i).css('left', left);
                if(i==layers.length-1){
                    $("#container_3d").width($("#img_"+i).width());
                    $("#container_3d").height($("#img_"+i).height());
                    max_position = -layer;
                }
            }
            // btn_go_left click
            $("#btn_go_left").click(function(){
                if(position>min_position) position --;
                adjust_layer();
            });
            // btn_go_right click
            $("#btn_go_right").click(function(){
                if(position<max_position) position ++;
                adjust_layer();
            });
                        
        });
        function adjust_layer(){
            for(var i=0; i<layers.length; i++){
                var layer = layers[i];
                var new_left = layer+position*(-layer/max_position);
                new_left = Math.round(new_left)
                $("#img_"+i).css('left', new_left);
            }
        }
    </script>
</head>
<body>
    <div id="container_3d"></div>
    <input type="button" id="btn_go_left" value="Left" />
    <input type="button" id="btn_go_right" value="Right" />
</body>