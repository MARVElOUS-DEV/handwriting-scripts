//完美排序

function perfectSort(arr,low,high)
{
	if(arr[low]>arr[high]) [arr[low], arr[high]]=[arr[high],arr[low]];
	if(high-low<=1) return;//关键在这个递归结束的条件
	var k= Math.floor((high-low+1)/3);
	perfectSort(arr,low,high-k);
	perfectSort(arr,low+k,high)
	perfectSort(arr,low,high-k)
}

const list = [3,5,6,1,2,8,7]
perfectSort(list, 0, list.length -1 )
console.log("🚀 ~ list:", list)
