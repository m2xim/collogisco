$(function () {
    var _filters = {
            _int_: [
                '<',
                '>',
                '=',
                '!=',
                '<=',
                '>='
            ],
            _str_: [
                '%',
                '='
            ],
            _dt_: [
                '<',
                '>',
                '=',
                '!=',
                '<=',
                '>='
            ]
        },
        _mapping_filter = {
            'BIGINT': _filters._int_,
            'INTEGER': _filters._int_,
            'VARCHAR(255)': _filters._str_,
            'DATETIME': _filters._dt_
        },
        _ejs_filter_item = new EJS({url: '/_static/ejs_tpl/filter_item.ejs.html'});

    $('.btn-add-fb-t').click(function () {
        var f_key_name = $('.select-key-fb-t option:selected').val(),
            f_column = f_columns[f_key_name],
            f_filters = _mapping_filter[f_column['type']];

        console.info('.btn-add-fb-t: Add filter for -> ' + f_key_name);
        console.log(f_column);
        console.log(f_filters);

        $('.fb-filters ul').prepend(_ejs_filter_item.render({
            _filters: f_filters,
            _column: f_column
        }));
    });

    $(document).on('click', '.btn-del-fb-f-i' ,function(){
        console.log('.btn-del-fb-f-i: Delete filter item.')

        $(this).parents('li').remove();
    });

});
