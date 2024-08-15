var $j = jQuery.noConflict();

function initializeAjaxUpdate(csrfToken, updateUrlTemplate) {
    $j(document).ready(function() {
        $j('.ajax-update').each(function() {
            $j(this).data('original-value', $j(this).val());
        });

        $j('.ajax-update').on('blur', function() {
            var element = $j(this);
            var value = element.val();
            var originalValue = element.data('original-value');
            var field = element.data('field');
            var id = element.data('id');

            // Only send AJAX if the value has changed
            if (value !== originalValue) {
                $j.ajax({
                    url: updateUrlTemplate.replace('0', id),
                    type: 'POST',
                    data: {
                        'name': field,
                        'value': value,
                        'csrfmiddlewaretoken': csrfToken
                    },
                    success: function(response) {
                        $j(element).data('original-value', value);
                    },
                    error: function(response) {
                        console.log('Error updating field:', response);
                    }
                });
            } else {
                console.log('No changes detected, request not sent.');
            }
        });

        $j('.ajax-update-select').on('change', function() {
            var element = $j(this);
            var value = element.val();
            var originalValue = element.data('original-value');
            var field = element.data('field');
            var id = element.data('id');

            // Only send AJAX if the value has changed
            if (value !== originalValue) {
                $j.ajax({
                    url: updateUrlTemplate.replace('0', id),
                    type: 'POST',
                    data: {
                        'name': field,
                        'value': value,
                        'csrfmiddlewaretoken': csrfToken
                    },
                    success: function(response) {
                        // Update the stored original value after a successful update
                        $j(element).data('original-value', value);
                    },
                    error: function(response) {
                        console.log('Error updating field:', response);
                    }
                });
            } else {
                console.log('No changes detected, request not sent.');
            }
        });
    });
}
