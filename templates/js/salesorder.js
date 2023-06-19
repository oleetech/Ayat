(function ($) {
    $(document).ready(function(){


        $('#id_CustomerName, #id_Address').on('change',function(){
            var initialname = $('#id_CustomerName').val();
            var initialquantity = $('#id_Address').val();
            if (initialname !== '' && initialquantity !== '') {
                $.ajax({
                    type: 'POST',
                    url: '/library/ajax/',
                    data: {
                        'name': initialname,
                        'quantity': initialquantity
                    },
                    dataType: 'json',
                    success: function(response){
                        // updateFormset(response);
                        // $('#id_production_components-0-quantity').val(response.quantity);

                    }
                });
            }

        });



    });
})(jQuery);