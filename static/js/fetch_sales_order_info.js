(function ($) {
    $(document).ready(function(){
        $('#id_name, #id_quantity').on('change',function(){
            var initialname = $('#id_name').val();
            var initialquantity = $('#id_quantity').val();
            if (initialname.trim() !== '' && initialquantity.trim() !== '') {
                $.ajax({
                    type: 'POST',
                    url: '/production/ajax/',
                    data: {
                        'name': initialname,
                        'quantity': initialquantity
                    },
                    dataType: 'json',
                    success: function(response){
                        updateFormset(response);
                        // $('#id_production_components-0-quantity').val(response.quantity);

                    }
                });
            }

        });
function updateFormset(data) {
  var formsetTable = $('table');
  formsetTable.empty();
    // Add table header
    var tableHeader = $('<thead>').appendTo(formsetTable);
    var headerRow = $('<tr>').appendTo(tableHeader);
    $('<th>').addClass('column-code required').text('Code').appendTo(headerRow);
    $('<th>').addClass('column-name required').text('Name').appendTo(headerRow);
    $('<th>').addClass('column-uom required').text('Uom').appendTo(headerRow);
    $('<th>').addClass('column-quantity required').text('Quantity').appendTo(headerRow);
    $('<th>').text('Delete?').appendTo(headerRow);
  
    // Add table body
    var tableBody = $('<tbody>').appendTo(formsetTable);
  data.forEach(function (component, index) {
    var row = $('<tr>');
    var codeCell = $('<td>');
    var codeInput = $('<input type="text" maxlength="20" class="vTextField">');
    codeInput.attr('name', 'production_components-' + index + '-code');
    codeInput.val(component.code);
    codeCell.append(codeInput);
    var nameCell = $('<td>');
    var nameInput = $('<input type="text" maxlength="100" class="vTextField">');
    nameInput.attr('name', 'production_components-' + index + '-name');
    nameInput.val(component.name);
    nameCell.append(nameInput);
    var uomCell = $('<td>');
    var uomInput = $('<input type="text" maxlength="20" class="vTextField">');
    uomInput.attr('name', 'production_components-' + index + '-uom');
    uomInput.val(component.uom);
    uomCell.append(uomInput);
    var quantityCell = $('<td>');
    var quantityInput = $('<input type="number" min="0" step="0.0001" required>');
    quantityInput.attr('name', 'production_components-' + index + '-quantity');
    quantityInput.val(component.quantity);
    quantityCell.append(quantityInput);

    var deleteCell = $('<td>');
    var deleteButton = $('<button>').text('Delete');
    deleteButton.addClass('delete-button');
    deleteButton.on('click', function() {
      // Handle delete button click
      row.remove();
    });
    deleteCell.append(deleteButton);   


    
    row.append(codeCell, nameCell, uomCell, quantityCell,deleteCell);
    formsetTable.append(row);
  });
  
}

          
          
    });
})(jQuery);

