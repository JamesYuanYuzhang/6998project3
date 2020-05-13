var apigClient = apigClientFactory.newClient({
			apiKey: "KSUzdjUzlL5AKM833eQTb28kWfemWQ6L6gnj5vED"
		});
$(document).ready(function() {
	$("#upload_button").click(() => {
		var f = $('#file_input').prop('files')[0];
		if (f) {
			console.log(f.name);
			console.log(f.type);
			console.log(f.size);
			if (!f.type.match('image.*')) {
				alert("Must be image");
				return false;
			}

			var params = {
			//This is where any header, path, or querystring request params go. The key is the parameter named as defined in the API
			"folder":"hw3.yy2979",
			"item":f.name,
			"Content-Type":f.type
			};
			console.log(f)

			// var body = {
			// 	f
			// };
			console.log(!body instanceof File)
			response=apigClient.folderItemPut(params, f)
			console.log(response)
		}
		else {
			alert("Please first select a file");
		}
	});
	$("#search_button").click(() => {
		//var q = $('#search_query').val();
		var q = $('#transcript').val();
		console.log(q);
		// var apigClient = apigClientFactory.newClient();
		var params = {
			//This is where any header, path, or querystring request params go. The key is the parameter named as defined in the API
			q: q
		};
		var body = {
			//This is where you define the body of the request
		};
		apigClient.searchgetGet(params, body).then(function(results){
			console.log(results)
			//This is where you would put a success callback
			$("ul").empty();
			for (var i in results.data)
			{
				var url=results.data[i]
				console.log(url)
				var img = "<li><img src=\"" + url + "\"></li>";
				$("ul").append(img);
			}
		}).catch(function(results) {
			//This is where you would put an error callback	

			console.log(results);
		});
	});
});




