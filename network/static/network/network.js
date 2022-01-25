document.addEventListener('DOMContentLoaded', function() {
	// document.querySelector('#heading').style.color = 'black';
	if (document.querySelector(".like")){
		var classes = document.querySelectorAll(".like");
		console.log(classes);
		
		for (let x = 0; x < classes.length; x++){
			let y=classes[x].value;
			
			classes[x].addEventListener('click', function (){
				
				console.log("id is " + y);
				// Note backticks
				fetch(`/like/${y}/`, {
			      method: 'PUT',
			    })
			    .catch((error) => {
			      console.log('Error:', error);
			    })
			    .then(res=>{
			    	let response = res.json()
			    	return response
			    })
			    .then(result=>{
			    	console.log(result.likes);
			    	let likes = document.getElementsByClassName(y);
			    	likes[0].innerHTML=result.likes;
			    });
				
			    
				
			});
		}
	}
	if (document.querySelector(".unlike")){
		let unlike_classes= document.querySelectorAll(".unlike");
		for (let x = 0; x < unlike_classes.length; x++){
			let y = unlike_classes[x].value;
			unlike_classes[x].addEventListener('click', function (){
				fetch(`/unlike/${y}/`, {
				      method: 'PUT',
				    })
				    .catch((error) => {
				      console.log('Error:', error);
				    })
				    .then(res=>{
				    	let response = res.json()
				    	return response
				    })
				    .then(result=>{
				    	console.log(result.likes);
				    	let likes = document.getElementsByClassName(y);
				    	likes[0].innerHTML=result.likes;
				    });
			  });  
		}
	}
	if (document.querySelector(".follow")){
		var classes = document.querySelectorAll(".follow");
		console.log(classes);
		
		for (let x = 0; x < classes.length; x++){
			let user_id=classes[x].value;
			let post_id=classes[x].name;

			
			classes[x].addEventListener('click', function (){
				
	
				// Note backticks
				fetch(`/following/${user_id}/`, {
			      method: 'PUT',
			      body: JSON.stringify({
            	  post_id: post_id,
            }),
			    })
			    .catch((error) => {
			      console.log('Error:', error);
			    })
			    .then(res=>{
			    	let response = res.json()
			    	return response
			    })
			    .then(result=>{
			    	console.log("result is " + result.follower);
			    	let follower = document.querySelectorAll(`.follow[name='${post_id}']`);
			    	let unfollower = document.querySelectorAll(`.unfollow[name='${post_id}']`);
			    	unfollower[0].style.display ="block";
			    	follower[0].style.display="none";
			    	// follower[0].style.color='blue';
			    	// follower[0].innerHTML='FOLLOWING';
			    });
				
			    
				
			});
		}
	}
	if (document.querySelector(".unfollow")){
		var classes = document.querySelectorAll(".unfollow");
		console.log(classes);
		
		for (let x = 0; x < classes.length; x++){
			let user_id=classes[x].value;
			let post_id=classes[x].name;
			
			
			classes[x].addEventListener('click', function (){
				
	
				// Note backticks
				fetch(`/unfollowing/${user_id}/`, {
			      method: 'PUT',
			      body: JSON.stringify({
            	  post_id: post_id,
            }),
			    })
			    .catch((error) => {
			      console.log('Error:', error);
			    })
			    .then(res=>{
			    	let response = res.json()
			    	return response
			    })
			    .then(result=>{
			    	console.log("result is " + result.follower);
			    	let unfollower = document.querySelectorAll(`.unfollow[name='${post_id}']`);
			    	let follower = document.querySelectorAll(`.follow[name='${post_id}']`);
			    	console.log(follower);
			    	unfollower[0].style.display ="none";
			    	follower[0].style.display="block";
			    });
				
			    
				
			});
		}
	}
	if (document.querySelector(".edit")){
		var classes = document.querySelectorAll(".edit");

		console.log(classes);
		
		for (let x = 0; x < classes.length; x++){
			let user_id=classes[x].value;
			let post_id=classes[x].name;
			
			classes[x].addEventListener('click', function editor(e){
				e.preventDefault();
				var formElem = document.createElement('form');
				var inputElem = document.createElement('textarea');
				inputElem.setAttribute('autofocus', 'autofocus');
				// inputElem.type = 'hidden';
				// inputElem.name = 'csrfmiddlewaretoken';
				// inputElem.value = '{{ csrf_token }}';
				formElem.appendChild(inputElem);
				classes[x].appendChild(formElem);
				inputElem.focus();
				
				let text=document.querySelector(`.content[name='${post_id}']`);
				inputElem.innerHTML=text.innerHTML;
				classes[x].removeEventListener('click', editor);
				let buttonElem=document.createElement('button');
				formElem.appendChild(buttonElem);
				buttonElem.innerHTML="Submit";
				buttonElem.addEventListener('click', function(e){
					e.preventDefault();
					let posting=inputElem.value;
					text.innerHTML=posting;
					fetch(`/edit/${post_id}/`, {
				      method: 'PUT',
				      body: JSON.stringify({
	            	  post_id: post_id,
	            	  text: posting
	                }),
				    })
				    .catch((error) => {
				      console.log('Error:', error);
				    })
				    .then(res=>{
				    	let response = res.json()
				    	return response
				    })
				    .then(result=>{
				    	console.log("JS result is " + result.text);
				    	classes[x].addEventListener('click', editor);
				    	formElem.remove();
				    });
				
			    
				
			    });
			});
				
		    }
	    }
    });





