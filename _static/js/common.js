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
                '=',
                '%',
                'not(%)',
                '= len(x)',
                '!= len(x)',
                '> len(x)',
                '< len(x)'
            ],
            _dt_: [
                '<',
                '>'
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

    $(document).on('click', '.btn-del-fb-f-i', function () {
        console.log('.btn-del-fb-f-i: Delete filter item.');
        $(this).parents('li').remove();
    });

    $(document).on('click', '.btn-submit-fb-t', function () {
        console.info('extract filters ...');
        var _filter_coll = [];
        $('.fb-filters ul').find('li').each(function () {
            var _filter_set = {
                f: $(this).find('.input-object-fb-f-i').attr('data-key'),
                c: $(this).find('.input-filter-fb-f-i option:selected').val(),
                v: $(this).find('.input-value-fb-f-i').val()
            };
            console.log(_filter_set);
            _filter_coll.push(_filter_set);
        });

        console.info('send filter collection ...');
        console.log(_filter_coll);

        $.ajax({
            url: '/api/get_by_filter',
            method: 'POST',
            dataType: 'html',
            data: {fcoll: JSON.stringify(_filter_coll)}
        }).done(function (msg) {
            $('.layer-tb_data').html(msg);
        });
    });

});
