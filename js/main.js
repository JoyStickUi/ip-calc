window.onload = function(){
	let sendFlag = false;
	let ipEl = document.getElementById('ip');
	ipEl.addEventListener('input', (event)=>{
		if(ipEl.value.match(/^\d+.\d+.\d+.\d+$/)){
			document.getElementById('netmask').style.display = "inline-block";
			document.getElementById('forNet').style.display = "inline-block";
		}else if(ipEl.value.match(/^\d+.\d+.\d+.\d+\/\d+$/)){
			document.getElementById('netmask').style.display = "none";
			document.getElementById('forNet').style.display = "none";
			sendFlag = ipEl.value.match(/^\d+.\d+.\d+.\d+\/\d+$/);
			document.getElementById('indicator').style.backgroundColor = "lime";
		}else{
			document.getElementById('netmask').style.display = "none";
			document.getElementById('forNet').style.display = "none";
			document.getElementById('indicator').style.backgroundColor = "red";
		}
	});

	let netmaskEl = document.getElementById('netmask');

	netmaskEl.addEventListener('input', (e)=>{
		sendFlag = netmaskEl.value.match(/^\d+.\d+.\d+.\d+$/) && ipEl.value.match(/^\d+.\d+.\d+.\d+$/);
		if(sendFlag){
			document.getElementById('indicator').style.backgroundColor = "lime";
		}else{
			document.getElementById('indicator').style.backgroundColor = "red";
		}
	});

	document.getElementById('submit').addEventListener('click', (event)=>{
		event.preventDefault();
		if(sendFlag){
			let ip = document.getElementById('ip').value;
			let netmask = document.getElementById('netmask').value;
			let url = 'http://172.17.3.128:80/ip?' + 'ip=' + encodeURIComponent(ip);
			if(netmask != ""){
				url += ",netmask=" + netmask;
			}
			fetch(url)
			.then(response=>response.json())
			.then(json=>{
				let table = document.getElementById('result');
				table.innerHTML = "";
				let matrix = [];
				for(let i = 0; i < json[1].length; ++i){
					matrix.push([]);
				}

				for(let i = 0; i < json.length; ++i){
					for(let j = 0; j < json[i].length; ++j){
						matrix[j].push(json[i][j]);
					}
				}

				for(let i = 0; i < json[1].length; ++i){
					let tr = document.createElement('tr');
					for(let j = 0; j < json.length; ++j){
						let td = document.createElement('td');
						td.textContent = matrix[i][j];
						tr.appendChild(td);
					}
					table.appendChild(tr);
				}
			});
		}
	});
}//192.168.32.1/10