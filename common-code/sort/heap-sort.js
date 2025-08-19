//第一步 创建大顶堆,创建的过程是一个数据冒泡的过程，大的数据会冒泡到根节点
function HeapSort(arr){
	var heapSize=arr.length;
	for(var i=Math.floor( heapSize/2 - 1 );i>=0;i--){
		heapAdjust(arr,heapSize,i);
	}

	while(heapSize>1){
		--heapSize;
		Swap(arr,0,heapSize);
		heapAdjust(arr,heapSize,0);
	}
}
//调整函数，是一个递归过程，每次对一个根节点调整的时候，会相应调整完以该节点i为根节点的所有的子节点
function heapAdjust(arr,heapSize,i){
	var t=i;
	var left=2*i+1;
	var right=2*i+2;
	if(left<heapSize && arr[left]>arr[t]){
		t=left;
	}
	if(right<heapSize && arr[right]>arr[t]){
		t=right
	}
	if(t!==i){
		Swap(arr,t,i)
		heapAdjust(arr,heapSize,t)
	}
}


function Swap(arr,i,j){
	var temp=arr[i];
	arr[i]=arr[j];
	arr[j]=temp;
}