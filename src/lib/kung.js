function getDominantSet(data){

	//take all keys except for id
	var allKeys = Object.keys(data[0]);

	keys = []

	allKeys.map(function(key){
		if (key !== "id"){
			keys.push(key);
		}
	})

	// console.log(keys);

	P = data.sort(function(a, b) {
	    return parseFloat(a[keys[0]]) - parseFloat(b[keys[0]]);
	});

	// console.log(keys);

	return front(P, keys);
}

function front(P, keys){

	// console.log(keys);

	if (P.length == 1){
		return P
	}else{
		var T = front(P.slice(0, Math.floor(parseFloat(P.length)/2)), keys);
		var B = front(P.slice(Math.floor(parseFloat(P.length)/2), P.length), keys);
		var M = [];
		
		for (var i = 0; i < B.length; i++) {
			// var keys = Object.keys(B[i]);
			var dominated = true;
			for (var j = 0; j < T.length; j++) {
				dominated = true;
				for (var k = 0; k < keys.length; k++) {
					// if target is not min, fac is -1 (reverse dominance criteria for maximization objective)
					fac = keys[k].indexOf("[min]") * 2 + 1
					if ((fac * parseFloat(B[i][keys[k]])) < (fac * parseFloat(T[j][keys[k]]))){
						dominated = false;
						break;
					}
				}
				if (dominated){
					break;
				}
			}
			if (!dominated){
				M.push(B[i]);
			}
		}
		return T.concat(M);
	}
}