# Conditonally Displaying Rows in a Table Based On Field Attribute

The default pop-up in AGOL works if all of the fields being displayed always have data to be displayed. In the case of the Over-the-Street Banners feature, hit does not work since it displayed all four directional street view fields in the pop-up even though ony two fields would have a link for any one location. The following code was created so that the pop-up would only display the relevant information for the direction of the banners which consisted of East/West and North/South pairs.

## Expression

It was determined 2 different expressions would be needed to cover both sets of cardinal directions. For the East and West directions, the following was used to check for either an East facing, a West facing, or an East or West facing banner location:

```js
If ($feature.BANNER_FACE_DIRECTION == "E - W" || $feature.BANNER_FACE_DIRECTION == "E" || $feature.BANNER_FACE_DIRECTION == "W") {
    return "table-row"
}
return "none"
```

For the North and South directions, the following was used to check for either a North facing, South facing, or North or South facing banner location:

```js
If ($feature.BANNER_FACE_DIRECTION == "N - S" || $feature.BANNER_FACE_DIRECTION == "S" || $feature.BANNER_FACE_DIRECTION == "N") {
    return "table-row"
}
return "none"
```

## Pop-up Configuration

For Pop-up Contents, the display choice in the dropdown was changed to "A custom attribute display". In the custom attribute display toolbar there is an option to use HTML for your pop-up, which lets you input HTML to control the way data is displayed in the popup. Field names are placed within {} to display the attribute for that record.

```html
<table cellpadding="0px" style="borderSpacing:1px 3px">
     <tbody>
           <tr valign="top">
               <td width="30%"><b>Location ID</b></td>
               <td width="70%"><span>{LOCATION_NAME}</span>
               </td>
            </tr>
            <tr valign="top">
               <td><b>Address</b></td>
               <td>{BANNER_ADDRESS}</td>
            </tr>
            <tr valign="top">
              <td><b>Description</b></td>
              <td>{DESCRIPTION_COMMON}</td>
            </tr>
            <tr valign="top">
              <td><b>Area</b></td>
              <td>{BANNER_AREA}</td>
            </tr>
            <tr valign="top">
              <td><b>Banner Face Direction</b></td>
              <td>{BANNER_FACE_DIRECTION}</td>
            </tr>
           <tr style="display:{expression/expr0}" valign="top">
               <td><b>EB Street View</b></td>
               <td><a href="{EB_STREET_VIEW}" target="_blank">More Info</a></td>
           </tr>
           <tr style="display:{expression/expr0}" valign="top">
               <td><b>WB Street View</b></td>
               <td><a href="{WB_STREET_VIEW}" target="_blank">More Info</a></td>
           </tr>
           <tr style="display:{expression/expr5}" valign="top">
               <td><b>NB Street View</b></td>
               <td><a href="{NB_STREET_VIEW}" target="_blank">More Info</a></td>
           </tr>
           <tr style="display:{expression/expr5}" valign="top">
               <td><b>SB Street View</b></td>
               <td> <a href="{SB_STREET_VIEW}" target="_blank">More Info</a></td>
           </tr>
      </tbody>
</table>
```

When the expression is met and "table-row" is returned the row will be displayed and when the expression is not met "none" will be returned and the row will not be displayed. This means consistent data entry for banners that can face either direction is needed so that the expression can be met when it should and correctly display the information for that record.