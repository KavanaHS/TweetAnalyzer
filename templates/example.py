😀
😐
☹
-----

'''
def admin(req):
    email=req.POST.get('username')
    subject=req.POST.get('pwd1')
    x=sub(name=subject,email=email)
    x.save()
    return render(req,'login.html')
'''


---------------------------


{% load static %}
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<center><h1> <u> Trending Tweet's :</center></u> </h1>
	<script src='https://cdn.plot.ly/plotly-2.8.3.min.js'></script>

<body>
	<form action="main">
		<h2>Search Based on Trending Place..?  💙💙💙<p style="font-size:68px;font-color:blue"></p> 
		<input type="text" name="keyword">
		<input type="submit" value="Search">

	</form>
	<style>
		table{
			padding-bottom: 2;

		}
		body{
           
            background-image:url(/static/images/gg.png);
            background-repeat: no-repeat;
             background-attachment: fixed;  
  background-size: cover;
          }

		Button{
			border-top-width: thick;
			  width: 20%;
		}
		input{
			font-family: Georgia, serif;
  border-collapse: collapse;
  font-size: 20px;
  width: 20%;
  height: 35px;
  text-align: center;
  font-style: oblique;
  padding-bottom: 2px;
		}
h1 {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}
h2{
	 color: black;
            font-style: bold;
            font-family: cursive;
}


td,th{
  border: 2px solid #dddddd;
  text-align: left;
  padding: 10px;
  font-size: 18px;

}
th{
	color: white;
}
tr:nth-child(even) {
  background-color: #dddddd;
}

</style>
<table>
	<th>Text</th><th>Sentimental</th>
	
	{% for i in ptweets %}
  <tr>
    <td>{{i.text}}</td>
    <td>{{i.sentiment}}</td>
    
  </tr>
	{% endfor %}
</td>
	<div id='chart' ></div>

		</table>

<center>
	<span>
		<button><a href="http://localhost:8000/" style="animation: step-end;"><h3>Back</h3></a></button>
	</span>
</center>
		
</body>

<script type="text/javascript">
	

	var data = [{
  values: {{values | safe}},
  labels: {{labels | safe}},
  type: 'pie'

}];

var layout = {
  height: 550,
  width: 1890,

    title:{
        text: "Tweet Report :",
        fontSize: 30,
      },
};

Plotly.newPlot('chart', data, layout);

</script>
</head>
</html>
