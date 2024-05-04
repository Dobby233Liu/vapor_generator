data = mydata

var scale = 2

// draw undusted part
draw_sprite_part_ext(
    sprite_index, image_index,
    0, line * scale,
    wd, sprite_height - line * scale,
    x, y + line * scale,
    image_xscale, image_yscale, c_white, 1
)

repeat (4)
{ // dust lines
    var line_x = x
    var code = 0

    while (code != ord("}") /* terminate line */ && code != ord("~"))
    {
        pos += 1
        code = ord(string_char_at(data, pos))

        var part_width = 0
        if (code >= ord("U") && code <= ord("U") + 36)
        { // black part, just skip over it
            part_width = code - ord("U")
            line_x += part_width * scale
        }
        else if (code >= ord("(") && code <= ord("(") + 42)
        { // white part
            part_width = code - ord("(")
            if (wd > 120)
            { // dust block
                /*var block = instance_create(line_x, y + line * scale, obj_npc_marker)
                block.visible = true
                block.sprite_index = spr_pixwht
                block.image_speed = 0*/
                var block = instance_create(line_x, y + line * scale, obj_whtpxlgrav)
                block.image_xscale = part_width
                line_x += part_width * scale
            }
            else repeat (part_width)
            { // indiviual dust
                /*var block = instance_create(line_x, y + line * scale, obj_npc_marker)
                block.visible = true
                block.sprite_index = spr_pixwht
                block.image_speed = 0*/
                instance_create(line_x, y + line * scale + scale /* ??? */, obj_whtpxlgrav)
                line_x += scale
            }
        }
    }

    /*var block = instance_create(line * 10, 0, obj_npc_marker)
    block.visible = true
    block.sprite_index = spr_undyneb2_spear
    block.image_speed = 0*/

    line += 1
    if (code == ord("~"))
    { // terminate dusting
        instance_destroy()
        exit
    }
}