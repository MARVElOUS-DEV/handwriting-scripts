


const quickSort = (arrInput, l, r) => {
  const partition = (arr, left, right) => {
    if (left === right) return left
    const pivotIndex = Math.floor(Math.random() * (right - left + 1)) + left
    const pivotValue = arr[pivotIndex];
    [arr[pivotIndex], arr[right]] = [arr[right], arr[pivotIndex]];
    let storeIndex = left
    for (let i = left; i < right; i++) {
      if (arr[i] > pivotValue) { // 降序排列
        [arr[storeIndex], arr[i]] = [arr[i], arr[storeIndex]]
        storeIndex++
      }
    }
    [arr[right], arr[storeIndex]] = [arr[storeIndex], arr[right]]
    return storeIndex
  }
  if (l < r) {
    const pivotIndex = partition(arrInput, l, r)
    quickSort(arrInput, l, pivotIndex - 1)
    quickSort(arrInput, pivotIndex+1, r)
  }
  console.log(arrInput)
}


// quickSort([3, 2, 1, 5, 4, 6], 0, 5)

// create a quick sort function
const quickSort2 = (arr) => {
  if (arr.length <= 1) return arr
  const pivotIndex = Math.floor(Math.random() * arr.length)
  const pivot = arr.splice(pivotIndex, 1)[0]
  const left = []
  const right = []
  for (let i = 0; i < arr.length; i++) {
    if (arr[i] < pivot) {
      left.push(arr[i])
    } else {
      right.push(arr[i])
    }
  }
  return quickSort2(left).concat([pivot], quickSort2(right))  // concat() 方法用于合并两个或多个数组。此方法不会更改现有数组，而是返回一个新数组。 
  }

  /**
   * 两路快排存在一个问题，当待排序列中存在较多的相同元素时，两路快排的效率会很低，因为每次划分只能将待排序列分成长度相差不多的两个子序列，而相同元素无法有效地划分。
   * 可以使用三路快排进行优化
   * https://developer.aliyun.com/article/1637195
   */


  // 目标使排序列中，小于pivot的元素放在左边，等于pivot的元素放在中间，大于pivot的元素放在右边
  function sortAndSwap(arr, left, right) { 
    const pivotIndex = Math.floor(Math.random() * (right - left + 1)) + left
    const pivotValue = arr[pivotIndex]
    let li=left, ri=right, m = left;
    [arr[pivotIndex], arr[right]] = [arr[right], arr[pivotIndex]];
    while(m < right && ri >=0) {
      if(arr[m] < pivotValue) {
        [arr[m], arr[li]] = [arr[li], arr[m]];
        li++;
        m++
      } else if(arr[m] > pivotValue) { // 当前元素大于pivotValue，放到后面，ri指针向前移动，但是cur指针不需要移动
        [arr[m], arr[ri]] = [arr[ri], arr[m]];
        ri--;
      } else { // m指向的元素与pivotValue相等，指针向后移动
        m++;
      }
    }
    [arr[li], arr[right]] = [arr[right], arr[li]];
    return [li, ri];
  };


  const quickSort3 = (arr, left, right) => {
    if(left >= right) return;
    // 每一次调用，都要选择一个pivot，并且完成将待排序列划分成三部分，分别对应小于pivotValue，等于pivotValue，大于pivotValue的元素
    const pivotIndex = Math.floor(Math.random() * (right - left + 1)) + left
    const pivotValue = arr[pivotIndex];
    let begin=left, end=right-1, cur = left;
    [arr[pivotIndex], arr[right]] = [arr[right], arr[pivotIndex]]; // 将pivot放到数组最后,也可放在最前面，循环结束最后需要交换回来
    while(cur <= end && end >=0) { // 因为m指针可能不移动，所以不能使用for循环迭代
      if(arr[cur] < pivotValue) {
        [arr[cur], arr[begin]] = [arr[begin], arr[cur]];
        begin++;
        cur++
      } else if(arr[cur] > pivotValue) { // 当前元素大于pivotValue，放到后面，end指针向前移动，但是cur指针不需要移动
        [arr[cur], arr[end]] = [arr[end], arr[cur]];
        end--;
      } else { // m指向的元素与pivotValue相等，指针向后移动
        cur++;
      }
    }
    [arr[begin], arr[right]] = [arr[right], arr[begin]];

    quickSort3(arr, left, begin-1)
    quickSort3(arr, end+1, right)
    console.log(arr)
  }

  // quickSort3([3, 2, 1, 5, 4, 6,9,8,7,10], 0, 9)

  var sortArray = function(nums) {
    const QSort = (nums, left, right) => {
      if (left< right) {
        const [begin, end] = pivot(nums, left, right)
        begin >=1 && QSort(nums, left, begin-1);
        end < right && QSort(nums, end+1, right);
      }
    }
    const pivot = (nums, left, right) => {
        if(left>=right) return [left,right];
        const p = Math.floor(Math.random()* (right-left+1))  + left;
        const pivotValue = nums[p];
        [nums[p], nums[right]] = [nums[right], nums[p]];
        let storeIndex = left, rightIdex =right-1;
        for(let i =left; i < right && storeIndex <= rightIdex; i++) {
            if(rightIdex>=0 && nums[i] < pivotValue) {
                [nums[storeIndex], nums[i]] = [nums[i], nums[storeIndex]];
                storeIndex++;
            } else if(rightIdex>=0 && nums[i] > pivotValue) {
                [nums[rightIdex], nums[i]] = [nums[i], nums[rightIdex]];
                i--;
                rightIdex--;
            }
        }
        [nums[storeIndex], nums[right]] = [nums[right], nums[storeIndex]];
        return [storeIndex,rightIdex];
    }
    QSort(nums,0, nums.length-1);
    return nums;
};

sortArray([3, 2, 1, 5, 4, 6,9,8,7,10])