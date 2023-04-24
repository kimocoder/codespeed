from django.core.exceptions import ValidationError


def validate_results_request(data):
    """
    Validates that a result request dictionary has all needed parameters
    and their type is correct.

    Throws ValidationError on error.
    """
    mandatory_data = [
        'env',
        'proj',
        'branch',
        'exe',
        'ben',
    ]

    for key in mandatory_data:
        if key not in data:
            raise ValidationError(f'Key "{key}" missing from GET request!')
        elif data[key] == '':
            raise ValidationError(f'Value for key "{key}" empty in GET request!')

    """
    Check that the items in integer_data are the correct format,
    if they exist
    """
    integer_data = ['revs', 'width', 'height']
    for key in integer_data:
        if key in data:
            try:
                rev_value = int(data[key])
            except ValueError:
                raise ValidationError(f'Value for "{key}" is not an integer!')
            if rev_value <= 0:
                raise ValidationError(
                    f'Value for "{key}" should be a strictly positive integer!'
                )
