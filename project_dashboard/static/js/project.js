/* Project specific Javascript goes here. */

/*
Formatting hack to get around crispy-forms unfortunate hardcoding
in helpers.FormHelper:

    if template_pack == 'bootstrap4':
        grid_colum_matcher = re.compile('\w*col-(xs|sm|md|lg|xl)-\d+\w*')
        using_grid_layout = (grid_colum_matcher.match(self.label_class) or
                             grid_colum_matcher.match(self.field_class))
        if using_grid_layout:
            items['using_grid_layout'] = True

Issues with the above approach:

1. Fragile: Assumes Bootstrap 4's API doesn't change (it does)
2. Unforgiving: Doesn't allow for any variation in template design
3. Really Unforgiving: No way to override this behavior
4. Undocumented: No mention in the documentation, or it's too hard for me to find
*/
// $('.form-group').removeClass('row');

(function() {
  document.querySelector('#categoryInput').addEventListener('keydown', function(e){
    // 13 is the keycode for the 'enter' key
    if (e.keyCode != 13){
      return;
    }

    e.preventDefault()

    var categoryName = this.value
    this.value = ''
    addNewCategory(categoryName)
    updateCategoriesString()
  })

  function addNewCategory(name){
    if (name == '') return;

    document.querySelector('#categoriesContainer').insertAdjacentHTML('beforeend',
      `<li class="category">
        <span class="name">${name}</span>
        <span onclick="removeCategory(this)" class="btnRemove bold">X</span>
      </li>`)
  }

})()

function fetchCategoryArray(){
  var categories = []

  document.querySelectorAll('.category').forEach(function(e){
    name = e.querySelector('.name').innerHTML
    if (name == '') return;

    categories.push(name)
  })

  return categories
}

function updateCategoriesString(){
  categories = fetchCategoryArray()
  document.querySelector('input[name="categoriesString"]').value = categories.join(',')
}

function removeCategory(e){
  e.parentElement.remove()
  updateCategoriesString()
}
