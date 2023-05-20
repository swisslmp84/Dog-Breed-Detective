	var allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;
	var selectedDogDescription = "";
	var recommendDescription1 = "";
	var recommendDescription2 = "";
	var recommendDescription3 = "";


	document.addEventListener('DOMContentLoaded', () => {
		const uploadBtn = document.querySelector('#uploadButton')
		const fileSelector = document.querySelector('#fileInput')

		uploadBtn.addEventListener("click", event => {
			if(fileSelector.files[0] == null){
				setErrorMessage("Please select a image file to upload!");
				return;
			}else if(!allowedExtensions.exec(fileSelector.files[0].name.toLowerCase())){
				setErrorMessage("Invalid file type! File extension jpg, JPEG, PNG is accepted!");
				return;
			}

			const API_ENDPOINT = "./uploadImage";
			const request = new XMLHttpRequest();
			const formData = new FormData();

			request.open("POST", API_ENDPOINT, true);

			document.querySelector('#recommendButton').hidden = true;
			document.querySelector('#resetButton').hidden = true;
			document.querySelector('#userDetail').hidden = true;
			document.querySelector('#userDetailDiv').hidden = true;
			document.querySelector('#dogDetailDiv').hidden = true;
			document.querySelector('#displayDiv').hidden = true;
			document.querySelector('#recommendationDiv').hidden = true;
			

			showPopUp();

			request.onreadystatechange = () => {
				if (request.readyState === 4 && request.status === 200) {
					const response = request.responseText;
					const results = JSON.parse(response)
					const imageMap = document.querySelector('#imageMap')

					imageMap.innerHTML = "";
					document.querySelector('#imageMessage').innerHTML = "<b>No dogs detected in image!</b>";

					if(results.length > 1){
						document.querySelector('#imageMessage').innerHTML = "<b>Click on dogs in image to show more info!</b>";
					}

					for (let i = 1; i < results.length; i++)
					{
						var element = document.createElement( "area" );
						element.shape = "rect";
						element.alt = results[i][0];
						element.coords = results[i][1] +"," + results[i][2] + "," + results[i][3] + "," + results[i][4];
						element.href="javascript:void(0);";
						element.addEventListener("click", event => {
							document.querySelector('#selectedheader').innerText = results[i][0];

							const GET_DOG_INFO_API_ENDPOINT = "./dogInfo?dogBreed=" + results[i][0] + "&nameType=Training_Dog_Breed";
							const request = new XMLHttpRequest();
							request.open("GET", GET_DOG_INFO_API_ENDPOINT);

							request.onreadystatechange = () => {
								if (request.readyState === 4 && request.status === 200) {
									const response = request.responseText;
									
									try {
										const dogInfo = JSON.parse(response);
										document.querySelector('#infoDiv').hidden = false;
										document.querySelector('#messageDiv').hidden = true;
										document.querySelector('#recommendMessage').hidden = true;
										document.querySelector('#recommendationDiv').hidden = true;

										selectedDogDescription = dogInfo["breed_description"];
										document.querySelector('#dogBreedDescription').value = selectedDogDescription;
										document.querySelector('#dogBreedGroup').innerHTML = dogInfo["breed_group"];
										document.querySelector('#dogSize').innerHTML = dogInfo["Dog_Size"];
										document.querySelector('#dogHeight').innerHTML = dogInfo["avg_height"];
										document.querySelector('#dogWeight').innerHTML = dogInfo["avg_weight"];
										document.querySelector('#dogLifespan').innerHTML = dogInfo["avg_lifespan"];
										document.querySelector('#dogOverallHealth').innerHTML = "<meter min='0' max='5' class='average-rating' style='--rating: " 
											+ dogInfo["overall_health"] + "' value='" + dogInfo["overall_health"] + "'></meter>";
										document.querySelector('#dogEasyToGroom').innerHTML = "<meter min='0' max='5' class='average-rating' style='--rating: " 
											+ dogInfo["easy_to_groom"] + "' value='" + dogInfo["easy_to_groom"] + "'></meter>";
										document.querySelector('#dogApartment').innerHTML = "<meter min='0' max='5' class='average-rating' style='--rating: " 
											+ dogInfo["apartment_friendly"] + "' value='" + dogInfo["apartment_friendly"] + "'></meter>";
										document.querySelector('#dogFamily').innerHTML = "<meter min='0' max='5' class='average-rating' style='--rating: " 
											+ dogInfo["family_friendly"] + "' value='" + dogInfo["family_friendly"] + "'></meter>";
										document.querySelector('#dogKid').innerHTML = "<meter min='0' max='5' class='average-rating' style='--rating: " 
											+ dogInfo["kid_friendly"] + "' value='" + dogInfo["kid_friendly"] + "'></meter>";
										document.querySelector('#dogDog').innerHTML = "<meter min='0' max='5' class='average-rating' style='--rating: " 
											+ dogInfo["friendly_to_others_dogs"] + "' value='" + dogInfo["friendly_to_others_dogs"] + "'></meter>";
										document.querySelector('#dogFirstTime').innerHTML = "<meter min='0' max='5' class='average-rating' style='--rating: " 
											+ dogInfo["good_for_1st_time_owners"] + "' value='" + dogInfo["good_for_1st_time_owners"] + "'></meter>";
										document.querySelector('#dogIntelligence').innerHTML = "<meter min='0' max='5' class='average-rating' style='--rating: " 
											+ dogInfo["intelligence"] + "' value='" + dogInfo["intelligence"] + "'></meter>";
										document.querySelector('#dogPlayfulness').innerHTML = "<meter min='0' max='5' class='average-rating' style='--rating: " 
											+ dogInfo["playfulness"] + "' value='" + dogInfo["playfulness"] + "'></meter>";

										
										document.querySelector('#userDetail').open = true;

								    } catch (e) {
								    	document.querySelector('#infoDiv').hidden = true;
										document.querySelector('#messageDiv').hidden = false;
										document.querySelector('#userDetail').hidden = true;
										document.querySelector('#recommendationDiv').hidden = true;
								    }
								}
							};

							request.send();

							resetAllUserInputFields();
							document.querySelector('#dogDetailDiv').removeAttribute("hidden");
							document.querySelector('#userDetail').removeAttribute("hidden");
							document.querySelector('#userDetailDiv').removeAttribute("hidden");
							document.querySelector('#recommendButton').removeAttribute("hidden");
							document.querySelector('#resetButton').removeAttribute("hidden");

							});

						imageMap.appendChild(element);
						
					} 

					document.querySelector('#displayDiv').removeAttribute("hidden");
					document.querySelector('#displayImage').src = encodeURI(results[0]);

					hidePopUp();
				}
				else
				{
					// setErrorMessage("Sorry the application is not responding please try again!");
					hidePopUp();
				}
			};
			formData.append("file", fileSelector.files[0]);
			request.send(formData);
		});
	});

	function showUserInputFields(){
		document.querySelector('#userDetailDiv').removeAttribute("hidden");
		document.querySelector('#userDetail').removeAttribute("hidden");
	}

	function showPopUp(){
		document.querySelector('#popup').style.display="block";
	}

	function hidePopUp(){
		document.querySelector('#popup').style.display="none";
	}

	function resetAllUserInputFields(){
		formElement = document.querySelector('#mainForm');
		formElement.reset();
		document.querySelector('#dogBreedDescription').value = selectedDogDescription;
		document.querySelector('#recommendImg1BreedDescription').value = recommendDescription1;
		document.querySelector('#recommendImg2BreedDescription').value = recommendDescription2;
		document.querySelector('#recommendImg3BreedDescription').value = recommendDescription3;
	}

	function displayRecommendation(recommendsStr, index){
		var recommendlist = recommendsStr.toString().split(",");
		var number1 = false;
		var number2 = false;
		var number3 = false;

		if(recommendlist.length != 0){
			for(let i=0; i<recommendlist.length; i++){
				if(recommendlist[i] != ''){
					if(i == 0)
						number1 = true;
					else if(i == 1)
						number2 = true;
					else if(i == 2)
						number3 = true;
				}

			}
		}

		
		if(!number1){
			document.querySelector('#recommendMessage').innerHTML = "<b>Sorry we can't find similar dog breed to recommend!</b>";
			document.querySelector('#recommendationDiv').hidden = true;
		}
		else{
			document.querySelector('#recommendMessage').innerHTML = "<b>Top 3 Recommendations!</b>";
		}

		document.querySelector('#recommendMessage').hidden = false;

		if(number1){
			document.querySelector('#recommendationDiv').hidden = false;
			document.querySelector('#recommendDetail1').hidden = true;
			document.querySelector('#recommendImgDiv2').hidden = true;
			document.querySelector('#recommendDiv2').hidden = true;
			document.querySelector('#recommendImgDiv3').hidden = true;
			document.querySelector('#recommendDiv3').hidden = true;
		}

		if(number1 || number2)
		{
			document.querySelector('#recommendDetail1').hidden = false;
			document.querySelector('#recommendDiv1').hidden = false;
		}

		if(number2 || number3)
		{
			document.querySelector('#recommendImgDiv2').hidden = false;
			document.querySelector('#recommendDiv2').hidden = false;
		}

		if(number3)
		{
			document.querySelector('#recommendImgDiv3').hidden = false;
			document.querySelector('#recommendDiv3').hidden = false;
		}

					
		itemNum = index + 1;

		if((itemNum == 1 && !number1) || (itemNum == 2 && !number2) || (itemNum == 3 && !number3))
			return;

			document.querySelector('#recommendLabel' + itemNum).innerHTML = "#" + itemNum + " : "  + recommendlist[index].toUpperCase();
			document.querySelector('#recommendImg' + itemNum).src = "./static/images/" + recommendlist[index] + ".PNG";

			const GET_DOG_INFO_API_ENDPOINT = "./dogInfo?dogBreed=" + recommendlist[index] + "&nameType=Dog_Breed";


			const request = new XMLHttpRequest();
			request.open("GET", GET_DOG_INFO_API_ENDPOINT);

			request.onreadystatechange = () => {
									if (request.readyState === 4 && request.status === 200) {
										const response = request.responseText;
										
										try {
											const dogInfo = JSON.parse(response);
											if(itemNum === 1)
												recommendDescription1 = dogInfo["breed_description"];
											else if(itemNum === 2)
												recommendDescription2 = dogInfo["breed_description"];
											else if(itemNum === 3)
												recommendDescription3 = dogInfo["breed_description"];

											document.querySelector('#recommendImg' + itemNum + 'BreedDescription').value = dogInfo["breed_description"];
											document.querySelector('#recommendImg' + itemNum + 'BreedGroup').innerHTML = dogInfo["breed_group"];
											document.querySelector('#recommendImg' + itemNum + 'Size').innerHTML = dogInfo["Dog_Size"];
											document.querySelector('#recommendImg' + itemNum + 'Height').innerHTML = dogInfo["avg_height"];
											document.querySelector('#recommendImg' + itemNum + 'Weight').innerHTML = dogInfo["avg_weight"];
											document.querySelector('#recommendImg' + itemNum + 'Lifespan').innerHTML = dogInfo["avg_lifespan"];
											document.querySelector('#recommendImg' + itemNum + 'OverallHealth').innerHTML = "<meter min='0' max='5' class='average-rating' style='--rating: " 
												+ dogInfo["overall_health"] + "' value='" + dogInfo["overall_health"] + "'></meter>";
											document.querySelector('#recommendImg' + itemNum + 'EasyToGroom').innerHTML = "<meter min='0' max='5' class='average-rating' style='--rating: " 
												+ dogInfo["easy_to_groom"] + "' value='" + dogInfo["easy_to_groom"] + "'></meter>";
											document.querySelector('#recommendImg' + itemNum + 'Apartment').innerHTML = "<meter min='0' max='5' class='average-rating' style='--rating: " 
												+ dogInfo["apartment_friendly"] + "' value='" + dogInfo["apartment_friendly"] + "'></meter>";
											document.querySelector('#recommendImg' + itemNum + 'Family').innerHTML = "<meter min='0' max='5' class='average-rating' style='--rating: " 
												+ dogInfo["family_friendly"] + "' value='" + dogInfo["family_friendly"] + "'></meter>";
											document.querySelector('#recommendImg' + itemNum + 'Kid').innerHTML = "<meter min='0' max='5' class='average-rating' style='--rating: " 
												+ dogInfo["kid_friendly"] + "' value='" + dogInfo["kid_friendly"] + "'></meter>";
											document.querySelector('#recommendImg' + itemNum + 'Dog').innerHTML = "<meter min='0' max='5' class='average-rating' style='--rating: " 
												+ dogInfo["friendly_to_others_dogs"] + "' value='" + dogInfo["friendly_to_others_dogs"] + "'></meter>";
											document.querySelector('#recommendImg' + itemNum + 'FirstTime').innerHTML = "<meter min='0' max='5' class='average-rating' style='--rating: " 
												+ dogInfo["good_for_1st_time_owners"] + "' value='" + dogInfo["good_for_1st_time_owners"] + "'></meter>";
											document.querySelector('#recommendImg' + itemNum + 'Intelligence').innerHTML = "<meter min='0' max='5' class='average-rating' style='--rating: " 
												+ dogInfo["intelligence"] + "' value='" + dogInfo["intelligence"] + "'></meter>";
											document.querySelector('#recommendImg' + itemNum + 'Playfulness').innerHTML = "<meter min='0' max='5' class='average-rating' style='--rating: " 
												+ dogInfo["playfulness"] + "' value='" + dogInfo["playfulness"] + "'></meter>";

											if(index < recommendlist.length){
												index = index + 1;
												displayRecommendation(recommendsStr, index);
											}

									    } catch (e) {
									    }
									}
								};

			request.send();	
	}

	function getDogRecommendation(){
		var name = document.querySelector('#selectedheader').innerText;
		name = name.slice(name.indexOf(':') + 1).trim();

		document.querySelector('#userDetail').open = false;
		document.querySelector('#recommendDetail1').open = false;
		document.querySelector('#recommendDetail2').open = false;
		document.querySelector('#recommendDetail3').open = false;

		const GET_DOG_RECOMMENATION_API_ENDPOINT = "./dogRecommendation?dogBreed=" + name 
			+ "&housing=" + document.querySelector('input[name="housingRadio"]:checked')?.value
			+ "&stayWithFamily=" + document.querySelector('input[name="familyRadio"]:checked')?.value
			+ "&hasKids=" + document.querySelector('input[name="kidsRadio"]:checked')?.value
			+ "&firstTimeOwner=" + document.querySelector('input[name="firstTimeRadio"]:checked')?.value
			+ "&hasOtherDog=" + document.querySelector('input[name="otherDogRadio"]:checked')?.value
			+ "&availableTime=" + document.querySelector('#userAvailableTime').value
			+ "&perferDogSize=" + document.querySelector('#preferDogSize').value
			+ "&perferCost=" + document.querySelector('#preferCost').value;

		const request = new XMLHttpRequest();
		request.open("GET", GET_DOG_RECOMMENATION_API_ENDPOINT);

		request.onreadystatechange = () => {
								if (request.readyState === 4 && request.status === 200) {
									const response = request.responseText;
									
									try {
										const recommendations = JSON.parse(response);
										displayRecommendation(recommendations,0);
										
										hidePopUp();
								    } catch (e) {
								    	
								    }
								}
								else
								{
									// setErrorMessage("Sorry the application is not responding please try again!");
									hidePopUp();
								}
							};
		showPopUp();
		request.send();	
	}

	function setErrorMessage(message){
		document.querySelector('#errorDiv').hidden = false;
		document.querySelector('#errorDiv').innerHTML = "<b>"+ message +"</b>";
	}

	function hideErrorMessage(){
		document.querySelector('#errorDiv').hidden = true;
	}