"""
Name: Sameera Balijepalli
"""
from pixelmagic import find_image
from pixelmagic import fade_image
from pixelmagic import grouped


#test cases for grouped
assert grouped([3,6,9,12,15,18,21]) == [[3, 6, 9], [12, 15, 18], [21]]
assert grouped([1,2,3,4,5,6,7,8,9,10]) == [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
assert grouped([]) == []


#test cases for find_image 
assert find_image([[1,2,3],[7,8,9],[4,5,6],[10,14,17]]) == [
    [10, 10, 10], [70, 70, 70], [40, 40, 40], [100, 100, 100]]
assert find_image([[0,0,0],[45,49,41],[91,97,80],[1,6,9]]) == [
    [0, 0, 0], [225, 225, 225], [225, 225, 225], [10, 10, 10]]
assert find_image(([[10,20,30],[40,50,60],[70,80,90],[100,110,120]])) == [
    [100, 100, 100], [225, 225, 225], [225, 225, 225], [225, 225, 225]]


#test cases for fade_image
assert fade_image([[1,2,3],[7,8,9],[4,5,6],[10,14,17]], 300, 100, 300,[20,21]) == [
    [0, 0, 0], [1, 1, 1], [0, 1, 1], [2, 2, 3]]
assert fade_image([[10,20,30],[45,49,60]], 150, 150, 150,[20,21]) == [
    [2, 4, 6], [9, 9, 12]]
assert fade_image([[10,20,30],[1,55,75]], 1, 10, 66,[20,21]) == [
    [8, 16, 25], [0, 47, 64]]
