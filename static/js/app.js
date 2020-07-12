$(document).ready(function(){
  function deleteUser(user_id){
    $.ajax({
      url: `/user/${user_id}`,
      type: 'DELETE',
      contentType: 'application/json',
      success: function(data){
        var url = `/?success=${data.success}`
        $(location).attr('href', url);
      }
    })
  }

  function updateUser(user_id, first_name, age){
    // Put the new user data
    let obj = {
      first_name: first_name,
      age: age,
      user_id: user_id
    }
    let json = JSON.stringify(obj);
    $.ajax({
      url: `/user/${user_id}`,
      type: 'PUT',
      contentType: 'application/json',
      data: json,
      success: function(data){
        var url = `/user/${user_id}?success=${data.success}`
        $(location).attr('href', url);
      }
    })
  }

  $('#delete-user').click(function(){
    var id = this.dataset.user_id;
    deleteUser(id);
  });

  $('#update-user').click(function(){
    var user_id = this.dataset.user_id;
    var first_name = $('#first_name').val();
    var age = $('#age').val();
    updateUser(user_id, first_name, age);
  })

})
