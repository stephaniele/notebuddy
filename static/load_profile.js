function load_profile(){
   
    

    var username = document.getElementById("Username").value
    var occupation = document.getElementById("Occupation").value
    var school = document.getElementById("School").value
    

    var user_data = [
        {"username":username},
        {"occupation":occupation},
        {"school":school}
    ]
    
    $.ajax({
        type: "POST",
        url: "/edit_profile",
        data: JSON.stringify(user_data),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
          var name = result.name;
          var school = result.school
          var occupation = result.occupation
          if (name.length > 0){
            document.getElementById("profile_name").innerHTML = name
          }
          if(school.length > 0){
            document.getElementById("profile_school").innerHTML = school
          }
          $("#ProfileModal").modal("hide")
        } 
    });
}