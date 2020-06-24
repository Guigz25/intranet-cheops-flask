
$(document).ready(function() {
    // $('#Success').hide();

    // Création d'un utilisateur 
    $('.container').on('click', '.add_member', function (){
        // On vide les champs lors de la création d'un utilisateur
        $('#formCreate').find('#nom').val('')
        $('#formCreate').find('#prenom').val('')
        $('#formCreate').find('#equipe').val("Choisir l'équipe parmie la liste")

        // On enleve l'alert d'erreur 
        $(".Error").hide();
    });

    $('#formCreate').on('click', '#valider_creation', function (){
    // $('#valider_creation').on('click',function(){
        var nom = $(this).parents('.modal-body').find('#nom').val()
        var prenom = $(this).parents('.modal-body').find('#prenom').val()
        var equipe = $(this).parents('.modal-body').find('#equipe option:selected').text()

         $.ajax({
            data: {
                type: "ajout",
                nom: nom,
                prenom: prenom,
                equipe: equipe
            },
            url: "/",
            method: "POST",
            })
            .done(function(data) {
                if (data.error) {
                    $(".Error").text(data.error).fadeIn();
                    $("#Success").hide();
                }
                else {
                    $('#formCreate').modal('hide');
                    $('.table').load(" .table")
                    
                    $("#Success").text(data['nomPrenom'] + ' a bien été ajouté').fadeTo(2000, 500).slideUp(500, function(){
                        $("#Success").slideUp(500);
                    });
                    
                }
            });
            

    });

    // Modification d'un user
    $('.container').on('click', '.update-form-button', function (){
         
        var nom = $(this).parents('.ligne').find('.nom').html()
        var prenom = $(this).parents('.ligne').find('.prenom').html()
        var equipe = $(this).parents('.ligne').find('.equipe').html()
        var index = $(this).parents('.ligne').find('.numIndex').html()

        $(".Error").hide();
        
        $('.formUpdateNom').val(nom)
        $('.formUpdatePrenom').val(prenom)
        $('#equipe option:selected').html(equipe)
        $('.formUpdateIndex').html(index)

    });
    $('#valider_modification').on('click',function(){
        // var nom = $(this).parents('.modal-body').find('#nom').val()
        // var prenom = $(this).parents('.modal-body').find('#prenom').val()
        // var equipe = $(this).parents('.modal-body').find('#equipe').val()

        nom = $('.formUpdateNom').val()
        prenom = $('.formUpdatePrenom').val()
        equipe = $('#equipe option:selected').html()
        index = $('.formUpdateIndex').html()

        $.ajax({
            data: {
                type: "update",
                nom: nom,
                prenom: prenom,
                equipe: equipe,
                index: index
            },
            url: "/",
            method: "POST",
            })
            .done(function(data) {
                if (data.error) {
                    $("#Error").text(data.error).fadeIn();                 
                    $("#Success").hide();
                }
                else {
                    $('#formUpdate').modal('hide');
                    $('.table').load(" .table")
                    $("#Warning").text(data['nomPrenom'] + ' a bien été modifié').fadeTo(2000, 500).slideUp(500, function(){
                        $("#Warning").slideUp(500);
                    });        
                }
            });
 
    });

    

    // Delete d'un user
    // $('.delete_button').on('click',function(){
    $('.container').on('click', '.delete_button', function (){

        var currentRow=$(this).closest("tr"); 
        var col1=currentRow.find("td:eq(0)").text();

        var nom = $(this).parents('.ligne').find('.nom').html()
        var prenom = $(this).parents('.ligne').find('.prenom').html()
        var equipe = $(this).parents('.ligne').find('.equipe').html()
        var index = $(this).parents('.ligne').find('.numIndex').html()

        
        $('.formDeleteNom').val(nom)
        $('.formDeletePrenom').val(prenom)
        $('.formDeleteEquipe').val(equipe)
        $('.formUpdateIndex').html(index)
        

    });
    
    $('.supprimer_utilisateur').on('click',function(){
        nom = $('.formDeleteNom').val()
        prenom = $('.formDeletePrenom').val()
        equipe = $('.formDeleteEquipe').val()
        index = $('.formUpdateIndex').html()

        $.ajax({
            url: "/",
            method: "POST",
            data: {
                type: "suppression",
                nom: nom,
                prenom: prenom,
                equipe: equipe,
                index: index
            },
            success: function(data) {
                $('#formDelete').modal('hide');
                $('.table').load(" .table > *")
                // location.reload();
                
                $("#Warning").text(data['nomPrenom'] + ' a bien été supprimé').fadeTo(2000, 500).slideUp(500, function(){
                    $("#Warning").slideUp(500);
                });
            }
            
        });
    });

    $('.gagnant-pp').on('click',function(){
        $.ajax({
            data: {
                type: "gagnant"
            },
            url: "/gagnant",
            method: "POST",
        })
        .done(function(data) {
                if (data['error']){
                    $(".Error-pp").text(data.error).fadeIn(); 
                }
                else{
                    // $('.gagnant-pp-body').html("<br>Le gagnant est : &emsp;" + data['gagnant']);
                    $('.formGagnant').val(data['gagnant'])
                    $('.formBackup').val(data['backup'])
                    // $('.backup-pp-body').html("Le backup est : &emsp;" + data['backup']);
                }
            });
        
    });
});


