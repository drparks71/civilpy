general_criteria = [
    {"label": "All Stage I comments resolved and detailed design is as per approved Stage I."},
    {"label": "All correspondence has been reviewed?"},
    {"label": "All bridge plan sheet are in order.", "reference": "BDM 103"},
    {"label": "Title block okay on all sheets? (As shown on Figure 102-4 in the Bridge Design Manual [BDM]) Designed," 
              "checked and reviewed blocks complete on all sheets?"},
    {"label": "Project number and bridge number correct?", "reference": "102.4"},
    {"label": "All lettering No. 5 or larger? Caps 5/32 inches in height) Sheets in an appropriate order? As per",
              "reference": "102.2"},
    {"label": "Supplemental Site Plan, if prepared during Stage 1 has not been included in plans?"},
    {"label": "Site Plan been checked with the final approved Sage 1 Site Plan? Deck transverse sections matches that "
              "approved in Stage I?"},
    {"label": "Call-outs are consistent on all sheets? (Span designation number, pier numbers, etc.)"},
    {"label": "North arrow shown on all plan views, all sheets.", "reference": "102"},
    {"label": "Each drilled shaft in the structure has been assigned a unique number?", "reference": "305.4.4"},
    {"label": "Each pile in the structure has been assigned a unique number?"},
    {"label": "Pier(s) and forward abutment elevations and the superstructure transverse section shown looking forward?"
              " Rear abutment elevation looking to the rear?", "reference": "102"},
    {"label": "Appropriate centerline/reference line used and referenced exclusively (consistent nomenclature) "
              "throughout the details."},
    {"label": "If an auxiliary reference line is established, is stationing given along this line only, near the "
              "bridge? Is a geometric diagram provided, if necessary?"},
    {"label": "For bridge with variable super-elevation, has a super-elevation transition diagram been provided?",
     "reference": "309.3.6.1 & 309.3.6.1a"},
    {"label": "Break over (1/2 inch per foot slope) provided on high side of superelevated decks for shoulder widths >4"
              " feet? Rounding beginning at edge of roadway used when change in cross slope at break over exceeds 3 "
              "percent 4-foot rounding for shoulders < 8 feet and 5 foot rounding for shoulders > 8 feet)?",
     "reference": "309.3.6.1 Figure 309-9 & 309-10"},
    {"label": "Approach slabs have been detailed as per Designer Supplement: AS-2-15-Approach Slab Installation?"},
    {"label": "Items that should be included with roadway quantities (e.g., Rock Channel Protection, Portable Concrete "
              "Barrier and Temporary Guardrail) have been designated as such?"},
    {"label": "Portions of existing structure that are to be removed have been properly indicated?"},
    {"label": "± Symbol used for existing structure dimensions? Dashed lines used to denote existing structures?",
     "reference": "207.4"},
    {"label": "Detail plans for temporary sheeting/shoring included if required by the", "reference": "310.1"},
    {"label": "Detail plans for a temporary runaround bridge included if required by the Scope?", "reference": "503"},
    {"label": "Concrete surfaces sealed per", "reference": "306.1.2, 309.2.1 and 403.3"},
    {"label": "Epoxy only sealer not used.", "reference": "309.2.1-G"}
],

site_plan_criteria = [
    {"label": "In the proposed structure data block verify the Latitude and Longitude.\nThe Latitude and Longitude of "
              "the begin Bridge limit station should be given to the nearest 0.01 second. The 0.01 second precision "
              "will be included in the next update."},
    {"label": "In the profile view provide the highest known high-water mark; normal water elevation and Ordinary "
              "High-Water Mark (OHWM).", "reference": "201.2.1"},
    {"label": "Show the length of the bedrock socket in the profile view.", "reference": "305.4.2"}
],

general_plan_criteria = [
    {"label": "Reference line shown for curved bridges, and stations should be shown where it intersects curve."},
    {"label": "Span lengths agree with Site Plan?", "reference": "202.1.1"},
    {"label": "Stage construction joint shown on appropriate plan views and details."},
    {"label": "Highway lighting feature shown, if applicable?"},
    {"label": "Scuppers shown, if applicable?"},
    {"label": "Approach drainage details (Gutters/catch basins)."},
    {"label": "Limits of slope protection."}
],

general_notes_criteria = [
    {"label": "All applicable general notes from BDM Section 600 included?"},
    {"label": "Wording of 'standard general notes' suit the project? (Do the notes make sense for this project?)"},
    {"label": "General notes included where necessary to describe 'as per plan' items?"},
    {"label": "In addition to the typical general notes given in the BDM, general notes are usually included to "
              "describe any 'non-standard' bid items or situations. Have these been included?"},
    {"label": "For rehabilitation projects, is the scope work itemized and clearly described under a PROPOSED WORK "
              "note?"},
    {"label": "Construction procedure for unusual conditions"}
],

detail_notes_criteria = [
    {"label": "See Section 700 of the Bridge Design Manual for a reminder list of typical detail notes."}
],


estimated_quantitites_criteria = [
    {"label": "All Items should be listed in the Estimated Quantities sheet in stage 2 without quantities."},
    {"label": "Pay-Item for cofferdam and excavation bracing included if required by section 310.1.1 of the BDM."}
],

reinforcing_details_criteria = [
    {"label": "Bar lengths conform to The maximum bar length should be approximately 40 feet. For longitudinal deck "
              "reinforcing, bar lengths of 30 feet are preferred, except for one odd length at end of run.",
     "reference": "304.4.1"},
    {"label": "Length of the short leg of L-shaped bars less than 8'-0\"?", "reference": "304.4.1"},
    {"label": "Minimum reinforcing steel provided in all faces of retaining walls and wall-type abutments and piers for"
              " shrinkage and temperature reinforcement?", "reference": "304.4.9 LRFD 5.10.6"},
    {"label": "Splice and development lengths for epoxy bars conform to current AASHTO requirements?",
     "reference": "LRFD 5.10.8"},
    {"label": "All bar splice lengths shown by plan note, on plan details, combination or reference?"},
    {"label": "Bridge seat reinforcement adequately clear of bearing anchors?", "reference": "306.2.1.2"},
    {"label": "Treatment of reinforcing steel appropriate at all construction, contraction, and expansion joints?",
     "reference": "306.2.5"},
    {"label": "Reinforcing steel in footings comply with (i.e., secondary rebars under main rebars, rebars at bottom of"
              " footing and not top of piles, dowel legs placed at bottom layer of footing rebars)?",
     "reference": "305.2.1.4"},
    {"label": "For cantilevered pier caps (T-type and cap and column), is the top layer of bars bent down the end face "
              "of the cap? Side faces adequately reinforced to resist longitudinal superstructure forces?",
     "reference": "306.3.3.3"},
    {"label": "Lateral ties between vertical bars in T-type and wall type piers as per section",
     "reference": "306.3.3"},
    {"label": "All reinforcing shall be epoxy coated?", "reference": "304.4"},
    {"label": "Letter prefix A (abutments), P (piers), S (superstructure), SP (spirals), DS (drilled shafts) generally "
              "used in bar marks?", "reference": "304.4.2"},
    {"label": "Mechanical connectors used where appropriate?", "reference": "304.4.4"},
    {"label": "Splices avoided at pier horizontal construction joints, except at top of footing?",
     "reference": "304.4.3"},
],

typical_sections_criteria = [
    {"label": "Large scale typical sections of existing and proposed superstructures provided to show removal and "
              "construction stages?"},
    {"label": "Location of cut lines and stage construction joints established with respect to primary survey line?"},
    {"label": "Typical section of existing structure conforms to current photographs and site inspection sketches?"},
    {"label": "Stage construction details sheet should include notes that detail the sequence of construction.",
     "reference": "309.3.8.5"}
],

part_plan_views_criteria = [
    {"label": "Part Plan views provided to show the relative relationship of the existing and proposed abutments during"
              " Stage 1 construction and relevant basic dimensions and clearances?"},
    {"label": "Sufficient room provided between temporary sheeting and proposed abutment for form construction and "
              "removal?"},
    {"label": "Sufficient room provided for pile driving?"}
],

temporary_sheeting_criteria = [
    {"label": "Consultant designed sheeting details provided in the plan when traffic is being maintained and the "
              "height of the retained earth is over 8 feet", "reference": "310.1.1.2"},
    {"label": "Temporary sheeting shown on the Site Plan and/or General Plan?"},
    {"label": "Cofferdams and Excavation Bracing item provided in quantities?"},
    {"label": "Tentative location of temporary sheeting shown on abutment plan views to retain backfill and permit "
              "partial removal and excavation for proposed construction?"}
],

temporary_railing_criteria = [
    {"label": "Reference for barrier details given to Standard Drawing PCB-91?"},
    {"label": "Barrier anchors provided not less than two per segment for barriers located less than 6'- 0\" from the "
              "edge of deck for bridges over roadways, railroad, or recreational areas: or less than 1'-0\" from the "
              "edge of the deck for other bridge application (PCB-DD)?"},
    {"label": "Double the number of anchor if the barrier location is less than 1 foot. (PCB-DD)?"},
    {"label": "Complete details given for temporary steel railing?"}
],

slab_bridges_criteria = [
    {"label": "Slab removal cut lines lie transverse to primary slab reinforcing steel?",
     "reference": "BDM201.2.6, 404.5"},
    {"label": "Temporary slab supports provided for such slabs", "reference": "310.1.2"},
    {"label": "Both stages of slab bridges supported by false work until second stage slab concrete has fully cured "
              "before false work is released (to avoid the use of a third stage closure section and high dead load "
              "shear forces on stage construction joints due to the premature release of false work)? (False work "
              "should be designed for live load)"}
],

lateral_restraint_criteria = [
    {"label": "Temporary lateral restraint provided to prevent rotational movement of the first stage superstructures "
              "of semi-integral bridges towards the unrestrained (no guide bearing) acute corners at stage construction"
              " joints?"},
    {"label": "For re-decking an existing structure without a closure section, a deck slab placement procedure provided"
              " requiring relatively complete second stage deck placement before placement of second stage integral"
              " end-diaphragms?"},
    {"label": "Semi-Integral Abutment Diaphragm Guide provided as per standard drawing SICD-2-14."}
],

end_dams_criteria = [
    {"label": "Full penetration butt-welded field splices provided at or near stage construction joints for "
              "superstructure portion of the end dams?"},
    {"label": "Bolted field splices provided for the abutment portion?"},
    {"label": "Offset between the two splices provided to facilitate butt-welding?"},
    {"label": "Superstructure splice located to clear beam flanges and cross frames gusset plates?"}
]

stage_cons_misc_criteria = [
    {"label": "Removal limits clearly shown or are apparent? Cross-hatching used to designate removal areas?"},
    {"label": "Removal Cut lines: Full-depth saw cut-lines specified for deck slab removals where the integrity of the"
              " slab is needed to support temporary railing? Cut-lines shown on plan and/or elevation views of"
              " substructure?", "reference": "201.2.6"},
    {"label": "Construction Access: Adequate space provided between Stage 1 construction and the remainder of the"
              " existing structure for temporary sheeting and form construction?"},
    {"label": "Closure Placements: 2'-6\" minimum wide third stage closure section provided for “new\" stringer "
              "superstructures?",
     "reference": "309.3.8.5"},
    {"label": "Are stage construction joints shown in all relevant views?"},
    {"label": "Cofferdam Sheeting: Vertical clearance available under 20 + feet) and/or adjacent to the existing "
              "structure to permit driving sheeting? Plan details shown tentative position of such sheeting where "
              "clearances are tight?"},
    {"label": "Provisions made for the complete or partial removal of temporary railing anchors and the grouting of "
              "resulting voids?"},
    {"label": "Roadway Item 614: Note provided referring to roadway plans for other temporary railing details and to "
              "Item 614 (roadway plans) for payment?"},
    {"label": "Approach slab details provided showing the same railing type as used on the bridge and with the same "
              "limiting edge clearances and/or anchorage (unless a different type of anchorage has been provided)?"},
    {"label": "Joint Type: An expansion or contraction joint used in lieu of a stage \"construction\" joint to simplify"
              " construction by eliminated lap splicing or mechanical connector splicing of reinforcing steel, where"
              " appropriate? (Abutment back walls, breast walls and certain pier walls, etc.)"},
    {"label": "Differential Shear: Vertical construction joints provided with shear keys and generous transverse "
              "reinforcement to resist the potentially high shear forces induced by differential deformation of "
              "foundations (piles, soil, etc.)? Formed joint surfaces artificially roughened to improve shear "
              "resistance",
     "reference": "LRFD 5.8.4"},
    {"label": "Battered Piles: Room adjacent to the existing structure to drive piles? Batter piles? New piles clear "
              "existing battered piles? Sufficient room available for pile length and leads to position batter piles "
              "for driving?"},
    {"label": "Screed Elevations: The presence or absence of cross frames at stage construction joints on stringer "
              "deflection taken into account when establishing screed elevations at stage construction joints."},
    {"label": "Integral Construction: Closure sections provided in bridges for both the deck slab and integral "
              "end-diaphragms?", "reference": "306.2.2.5"},
    {"label": "Elastomer Seals: Note provided requiring seals for each joint to be installed in one continuous "
              "piece?"},
    {"label": "Drain Pipes: Abut porous backfill drain pipes terminated and capped on both sides of temporary "
              "sheeting?"},
    {"label": "Utility conduits located clear of stage construction joints and temporary sheeting?"},
    {"label": "The design for adhesive concrete anchors shall be in accordance with AASHTO LRFD Section 513."}
]

slab_criteria = [
    {"label": "Sealing of concrete surfaces shown and appropriate?", "reference": "306.1.2"},
    {"label": "Stainless steel drip strip provided on decks with over-the-side drainage?",
     "reference": "309.2 and 309.7"},
    {"label": "Verify reinforcing steel accommodate HL-93 loading."},
    {"label": "Lap lengths to other bars."},
    {"label": "Centerline of bearing stations"},
    {"label": "Continuous Deck Slab Placement Detail.", "reference": "ODOT STD. DWG. PSID-1-13"}
]

prestressed_concrete_box_criteria = [
    {"label": "For multiple span bridges, has the superstructure been detailed as continuous as per Standard Drawing "
              "PSBD-2-07?", "reference": "308.2.3.3"},
    {"label": "Multiple span bridges of less than 200-foot total length with flexible piers and abutments fixed at all "
              "substructure units?"},
    {"label": "Standard Drawings PSBD-2-07 has been reviewed and items required by it provided? It is not intended that"
              " details and notes shown on the Standard Drawing be repeated unnecessarily."},
    {"label": "All beams anchored?", "reference": "308.2.3.3f"},
    {"label": "Membrane waterproofing (Type 3) used on all non-composite box beam Bridge?", "reference": "308.2.3.3d"},
    {"label": "For bridge with poured sealant joints, has waterproofing been extended 2 feet past the bridge limits?",
     "reference": "CMS 512.08H"},
    {"label": "Two-inch spacing or multiple thereof provided between strands? If space permits, place all strands in "
              "bottom row.", "reference": "302.5.1.2.b"},
    {"label": "Location, length, and number of debonded strands shown?", "reference": "308.2.3.4a"},
    {"label": "Additional strand debonding and supplemental mild reinforcing steel provided at beam ends for skews over"
              " 30 degrees? Limit box beam to 30-degree skew or less except rare occasions approved by Office of "
              "Structural Engineering."},
    {"label": "Strands and rebars miss anchor, diaphragm, and bearing rod holes? Are there any conflicts between "
              "strands, rebars, tie-rod holes, beam anchor rod holes, rail post anchors, joint armor, etc.?",
     "reference": "PSBD-2-07"},
    {"label": "PEJF specified as grout retainer at dowels and under beam connection at piers?",
     "reference": "Standard Drawing PSBD-2-07"},
    {"label": "Two bearings provided for each box beam?", "reference": "308.2.3.3"},
    {"label": "Proper camber/wearing surface notes used?", "reference": "702.7"},
    {"label": "Wearing surface/composite topping thickness diagram shown?", "reference": "308.2.3.4b"},
    {"label": "If over-the-side drainage will occur, has a drip strip been specified? Reference should be made to "
              "Standard Drawing DS-1-92."},
    {"label": "Sealing of concrete surfaces provided as directed in", "reference": "309.2.1.D"},
    {"label": "Shear key mortar finishing detail shown? (Not required for composite concrete decks)",
     "reference": "PSBD-2-07"},
    {"label": "Sufficient dimensions furnished for the beam fabricator to locate the railing post anchors? Have "
              "location of inserts for stage construction temporary railing shown? Has conflict between post anchors "
              "and tie rods and/or T-section been avoided?", "reference": "308.2.3.3"},
    {"label": "Proper allowances for fit-up between beams accounted for and shown?", "reference": "308.2.3.3"},
    {"label": "Maximum of three beams tied together by one tie-rod?", "reference": "PSBD-2-07"},
    {"label": "Transverse tie-rods provided at abutment ends and located per", "reference": "308.2.3.3g"},
    {"label": "For non-composite design, is asphalt thickness 8 inches or less?", "reference": "308.2.3"},
    {"label": "For multiple span bridges, has the same beam depth been specified for all spans?", "reference": "308.2.3"},
    {"label": "For beams greater than 100 ft. long, for concrete release strength greater than 5 ksi, and for 28 days "
              "concrete strength greater than 7 ksi, provide a letter per", "reference": "308.2.3"},
    {"label": "Strand location and clearance consistent with PSBD-2-07."},
    {"label": "Diaphragms and tie rods located", "reference": "308.2.3.3g"},
    {"label": "For composite box beams, six-inch minimum slab thickness specified?", "reference": "308.2.3.3.c"},
    {"label": "No. 6 at 18 inches longitudinal and No. 6 at 9 inches transverse bars specified",
     "reference": "308.2.3.3.c"},
    {"label": "Additional bars over piers specified to meet the requirements of",
     "reference": "308.2.3.3.c and LRFD 5.10.8.1.2c"},
    {"label": "Epoxy coated bars (Grade 60) specified in the composite slab?", "reference": "304.4"},
    {"label": "Bars projecting from beam into composite slab specified as epoxy coated?", "reference": "304.4"},
    {"label": "Construction joint shown between the cast-in-place 'T' section at piers and the composite slab?"},
    {"label": "The effect that the longitudinal grade has on dimensions measured along a beam’s length addressed in the"
              " plans?", "reference": "308.2.3.2"},
    {"label": "Verify that design uses severe corrosive factor as per Section S.5.9.2.3.2b by changing the design "
              "parameter in Conspan. The limiting stress factor for tension (service III) should be .0948 instead of "
              "0.19."}
]

steel_stringers_criteria = [
    {"label": "Are the proposed beam shapes per", "reference": "308.2.3.4"},
    {"label": "Low-relaxation, 270 ksi, 0.6-inch strands used? (Initial stress = 0.75 f’s)",
     "reference": "304.5.1, 304.5.2"},
    {"label": "Straight strands, debonded at ends if necessary, used? Draped strands should be provided as per",
     "reference": "308.2.3.3.a 308.2.3.4.a.3"},
    {"label": "No more than 25% of the total strands debonded?", "reference": "302.5.2.2.h"},
    {"label": "No more than 45% of the strands in any row debonded", "reference": "302.5.2.2.d"},
    {"label": "Number and spacing of debonded strands, and the length of debonding, shown?", "reference": "302.5.2.2.d"},
    {"label": "Strand location and spacing meet requirements of", "reference": "308.2.3.3.b"},
    {"label": "Initial prestressed loads shown in the plans", "reference": "304.5.2"},
    {"label": "Joint details appropriate? Details from Standard Drawings EXJ-6-06."},
    {"label": "Grade 60 mild reinforcing used?", "reference": "304.4"},
    {"label": "Bars projecting from I-beam been epoxy coated?", "reference": "304.4"},
    {"label": "Diaphragms placed at intervals not exceeding 40 feet", "reference": "308.2.3.4.d"},
    {"label": "Intermediate diaphragms do not make contact with the underside of the deck?", "reference": "308.2.3.4.d"},
    {"label": "End diaphragms make complete contact with the underside of the deck?", "reference": "308.2.3.4.d"},
    {"label": "Threaded inserts used to connect diaphragm rebars to beams? Type and coating requirements for inserts "
              "shown?", "reference": "308.2.3.4.d"},
    {"label": "Note provided restricting deck placement to a minimum of 48 hours after diaphragms are placed and cured?"
              " If the Standard Bridge Drawing for I-beams is not referenced by the contract plans",
     "reference": "308.2.3.4.d"},
    {"label": "Bridge seat elevations been computed as directed in", "reference": "308.2.3.4.b"},
    {"label": "Diagram provided showing slab thickness at center of each span and at each centerline of bearings?",
     "reference": "308.2.3.4.b"},
    {"label": "Beam anchorage meets the requirements of", "reference": "308.2.3.4.c"},
    {"label": "Full-depth cast-in-place concrete deck specified/ precast deck panels should not be used.",
     "reference": "309"},
    {"label": "Threaded insert location shown on the beam elevation view for draped strands.", "reference": "PSID-1-13"},
    {"label": "The longitudinal superstructure cross section in the plans detailing the total topping thickness, "
              "including the design slab thickness and the haunch thickness at the centerline of spans and bearings.",
     "reference": "308.2.3.4.b"},
    {"label": "Camber at the time of release, at the time of erection, long term camber and a screed elevation table "
              "shown", "reference": "308.2.3.4.b"},
    {"label": "Verify that design use severe corrosive factor as per Section S.5.9.2.3.2b by changing the design "
              "parameter in Conspan. The limiting stress factor for tension (service III) should be .0948 instead of "
              "0.19"}
]

steel_stringers_general_criteria = [
    {"label": "A709 Grade 50W steel shall be specified for un-coated weathering steel bridges, A709 Grade 50 specified "
              "for a coated steel bridge.", "reference": "30.4.1"},
    {"label": "A709 Grade 50W structural steel within 10 feet from end of stringer adjacent to deck joint painted and "
              "note provided", "reference": "308.2.2.1.d.1"},
    {"label": "Proper painting system used? Formerly called, System IZEU on new steel and System OZEU on existing "
              "steel?", "reference": "308.2.2.1.d.1"},
    {"label": "All main load carrying members such as rolled beams, girder web/flanges, moment plates, splice plates, "
              "and horizontally curved stringer cross frames designated as CVN for Charpy V-notch testing and plan note"
              " provided?", "reference": "308.2.2.1.b and 702.2"},
    {"label": "Clearance between the bottom mat and top of the bolt over splice plate."},
    {"label": "Steel fabricator certification given in pay item description as Classification Levels 1 thru 6, SF or "
              "UF.", "reference": "308.2.2.1.b"},
    {"label": "Cross frames and field splices for dog-legged (deflected) stringers conform with, Additional horizontal "
              "cross frames angle provided near top flange of horizontally curved stringers?",
     "reference": "308.2.2.1.j, 308.2.2.1.j.1 and 308.2.2.2.b"},
    {"label": "Plan note provided for High Strength Bolts?", "reference": "702.3"},
    {"label": "Leg size specified for fillet welds 1/4 inch minimum for material < 3/4 inch thick and 5/16 inch minimum"
              " for thicker material)?", "reference": "308.2.2.2.c.1"},
    {"label": "Complete penetration groove welds designated as CP with weld configuration left unspecified? Partial "
              "penetration groove welds not permitted on structural elements.",
     "reference": "308.2.2.2.c and ANSI/AASHTO / AWS D1.5 Bridge Welding Code"},
    {"label": "Stud shear connectors preferably 7/8 inch diameter and uniformly spaced transversely not closer than 4 "
              "diameters center to center with at least 1 inch clearance from flange edges? (Typically, three studs "
              "transversely for flanges 12 inches and wider)", "reference": "404.1.6 & AASHTO LRFD 6.10.10"},
    {"label": "Shear connector length penetrates at least 2 inches above bottom reinforcing steel of slab and provides "
              "at least 2 inches top cover?"},
    {"label": "7/8 inch diameter Shear stud not recommended for vertical application due to longer welding times and "
              "difficulties. Use a 3/4 inch diameter shear stud recommended by the industry."},
    {"label": "Shear connector maximum spacing generally not greater than 24 inches? Usually, fatigue and strength "
              "criteria produce maximum spacing near piers, smallest spacing near abutments, and moderate spacing near "
              "mid spans? No conflict near field splices or deck joint anchorage?", "reference": "AASHTO LRFD 6.10.10"},
    {"label": "Extra shear connectors provided at contra flexure points and longitudinal slab reinforcement properly "
              "extended if shear connectors are omitted over piers?", "reference": "AASHTO LRFD 6.10.10"},
    {"label": "Field splices located near points of dead load contra flexure as appropriate to facilitate erection and "
              "to limit field section lengths to 90 feet maximum for rolled beams and 120 feet maximum for plate "
              "girders? Additional optional field splices may be shown recognizing greater availability of short "
              "lengths)", "reference": "308.2.2.1.c and 308.2.2.1.j.3"},
    {"label": "Plate thicknesses specified in the following standard sizes: 7/8\" to 3” In 1/8” Increments, 3\" And "
              "above 1/4\" Increments?", "reference": "308.2.2.3.c"},
    {"label": "Buoyant superstructures typically integral or semi-integral designs) where inundation is possible "
              "details with appropriate countermeasures (e.g., holes drilled in stringer webs for egress of confined "
              "air, support anchorage, etc.)?"},
    {"label": "Stringer top flange compression and tension zones shown and Welded Attachment Note provided?",
     "reference": "702.11"},
    {"label": "Camber and deflection table provided for information given at center of spans, splices points, and at 25"
              " foot maximum intervals?", "reference": "702.1, 309.3.3"},
    {"label": "Camber diagram provided and blocking dimension from bottom of stringer at each support to chord between "
              "end supports) shown?", "reference": "309.3.3"},
    {"label": "Camber adjustment provided for horizontally heat-curved stringers and for straight stringers on curved "
              "bridges?", "reference": "AASHTO LRFD 6.7.7"},
    {"label": "Sign (direction) of camber adjustment for vertical curve correct?"},
    {"label": "Edge distances used for field splices as per LRFD table 6.13.2.6.6-1?",
     "reference": "308.2.2.1.j.1 & 308.2.2.1.j.2"},
    {"label": "For galvanized structures, the bolt hole size requires a 1/16 inch increase.",
     "reference": "308.2.2.1.j.1"},
    {"label": "Field splices located so as not to interfere with other details (i.e., intermediate stiffeners, cross "
              "frames, etc.)?", "reference": "308.2.2.2.b"},
    {"label": "Fatigue prone details avoided if possible?", "reference": "308.2.2.1.g"},
    {"label": "Cross frame connection stiffeners rigidly attached to stringer top and bottom flanges?",
     "reference": "308.2.2.2.a"},
    {"label": "Lateral bracing provided only when required?", "reference": "AASHTO LRFD 6.7.5"},
    {"label": "Curved girder with stage construction should be checked for deflection at each stage."}
]

rolled_beams_criteria = [
    {"label": "Welded moment plates not used in areas of tensile stress?", "reference": "308.2.2.2.d"},
    {"label": "Bearing stiffeners provided only when necessary?", "reference": "AASHTO LRFD 6.10.11.2"},
    {"label": "Galvanized beams limited in length to 60 feet maximum and utilize bolted connections only?",
     "reference": "308.2.2.1.d.2"}
]

plate_girders_criteria = [
    {"label": "Top flange width as per", "reference": "308.2.2.3.c.1"},
    {"label": "Flange thickness at least 7/8 inch?", "reference": "308.2.2.3.c.1"},
    {"label": "Web thickness and stiffener thickness at least 3/8 inch", "reference": "308.2.2.3.c.2"},
    {"label": "Flange butt welds subject only to compressive stresses identified as CS and complete joint penetration "
              "as CP.", "reference": "308.2.2.3.f.2"},
    {"label": "Non-redundant main steel members identified as FCM (Fracture Critical Member)? Proper pay item and plan "
              "note provided", "reference": "BMD 308.2.2.3.b"},
    {"label": "Longitudinal stiffeners not used? Transverse stiffeners preferably not used (except cross frame "
              "connection stiffeners)", "reference": "308.2.2.3"},
    {"label": "Transverse stiffeners (if used) placed on alternate sides of interior girders and inside face only of "
              "fascia girders, made same size throughout, and detailed?", "reference": "308.2.2.3.d"},
    {"label": "Cross frame connection stiffeners fillet welded to web and both flanges", "reference": "308.2.2.3.d"},
    {"label": "Bearing stiffeners made to extend as near as practicable to outer edges of flange plate and detailed as "
              "tight fit at top flange, mill to bear at bottom flange? (Rigid attachment to both flanges may be "
              "appropriate if used also as a connection plate)", "reference": "AASHTO LRFD 6.10.11.2.1 / LRFD 6.10.11.2"},
    {"label": "Intermediate cross frame angle size and connections conform with STD DWG GSD-1-19? For beam/Girder D < 6"
              " feet."},
    {"label": "Constant flange widths used whenever possible? Make changes in flange width at field splice to "
              "facilitate fabrication. Changes in flange plate section appropriate based on cost criteria given in",
     "reference": "308.2.2.3.c.1 Steel Bridge Design Handbook FHWA-IF-12-052-Vol. 6"},
    {"label": "Clearance between the bottom mat and top of the bolt over splice plate", "reference": "309.3.4.2"}
]

concrete_deck_on_stringers_criteria = [
    {"label": "Verify bottom concrete cover of bars in the overhang deck", "reference": "LRFD 5.10.1, 304.4.8"},
    {"label": "Sealing of concrete surfaces shown and appropriate", "reference": "309.2.1"},
    {"label": "Stainless steel drip strip provided on decks with over-the-side drainage?",
     "reference": "309.7 and 309.2"},
    {"label": "Deck slab depth over stringers shown to top of web for plate girders and to top of flange for rolled "
              "beams or prestressed concrete I-beams and plan note provided", "reference": "702.5 and 702.6"},
    {"label": "2-inch minimum concrete haunch depth used over stringers (top of thickest flange section to bottom of "
              "slab)", "reference": "309.3.5"},
    {"label": "For steel beam or girder bridges with skew less than 15 degrees the transverse bars parallel to abutment"
              " and for skew more than 15 degrees or interference with shear stud, transverse bars placed perpendicular"
              " to the centerline of bridge.", "reference": "309.3.4.2"},
    {"label": "For prestressed I-beam or composite box beam bridge deck, transverse bars perpendicular to the "
              "centerline of bridge.", "reference": "309.3.4.2"},
    {"label": "Slab thickness and reinforcement conform to", "reference": "Figure 309-3, 309-4 or 309-5"},
    {"label": "Top and bottom main (transverse) bars at same spacing and placed to coincide in a vertical plane?",
     "reference": "309.3.4.2"},
    {"label": "Transverse bars placed parallel to abutments for bridges with skews less than 15 degrees?",
     "reference": "309.3.4.2"},
    {"label": "Length of transverse bars without lap splices 5 inches shorter than deck (edge to edge distance) to "
              "ensure adequate cover at ends of bar, allowing for shop cutting tolerances?"},
    {"label": "(Transverse) bars", "reference": "309.3.4.1"},
    {"label": "Secondary (longitudinal) bars placed above main", "reference": "309.3.4.1"},
    {"label": "Additional top longitudinal bars with ends staggered 3'-0\" provided over piers on continuous "
              "structures? Total longitudinal reinforcement meets the requirements of AASHTO LRFD 6.10.1.7 for steel "
              "stringers or for prestressed concrete I-beam? Generally, No. 6 bars midspaced between top full length "
              "longitudinal bars will be adequate and will provide enough clearance between bars to facilitate concrete"
              " placement and vibration.", "reference": "308.2.3.3.c"},
    {"label": "Screed elevations given along curb lines/edges of deck, roadway crown, transverse grade-break lines and "
              "phase construction lines at all bearings, quarter-span, mid-span, and splice points, plus any points "
              "required for a maximum 25 foot spacing.", "reference": "309.3.3.1"},
    {"label": "Slab pour sequence generally specified only when uplift during construction or differential deflections "
              "at intermediate expansion joints are of concern.", "reference": "2.2.3.g, 403.5.4"},
    {"label": "Check three independent sources of girder twist resulting from deck placement: global superstructure "
              "distortion, oil-canning and girder warping.", "reference": "309.3.8.2"},
    {"label": "Neglect girder twist due to global deformation if the tributary deck load carried by the fascia girder "
              "is less than 110% of the average of the tributary deck load carried by the interior members for new "
              "structure and 115% for existing structure.", "reference": "309.3.8.2.a"},
    {"label": "For web depth greater than 84 inches note for location of lower contact point of the overhang false work"
              " included.", "reference": "611.4.1"},
    {"label": "Screed, top of haunch and finished deck surface shown and note included?",
     "reference": "309.3.3.1, 309.3.3.2, 309.3.3.3, 702.12.1, 702.12.2, 702.12.3"},
    {"label": "The final deck surface elevation locations should be identified in a plan view.",
     "reference": "309.3.3.3"},
    {"label": "The screed elevation locations should be identified on the transverse section.", "reference": "702.12.1"},
    {"label": "The top of haunch elevation locations should be identified on the transverse section.",
     "reference": "702.12.2"},
    {"label": "Deck placement design assumptions note is included.", "reference": "611.4.2"}
]

deep_beam_railing_criteria = [
    {"label": "Deep beam guardrail must be used in accordance with", "reference": "309.4.3.4"}
]

twin_steel_tube_criteria = [
    {"label": "Reference to Standard Drawing. TST-1-99 Given."},
    {"label": "Pay limits for bridge railing measured center-to-center of the second posts on the approaches?"},
    {"label": "Rail post spacing of 6'-3\" c/c of post maintained except one post spacing per span can be decreased to"
              " allow for construction clearances."},
    {"label": "Suitable clearances between posts and back walls and between post anchors and expansion joint armor "
              "anchors provided?"},
    {"label": "Wing-wall mounted post used to provide suitable post and anchor bar clearances?"},
    {"label": "For box beam bridges with steel railing, the post spacing and position of post anchorage shall be "
              "detailed on the plans."},
    {"label": "Enlarged details provided to describe post anchorage to composite box beams?"}
]

sidewalk_with_conc_para_criteria = [
    {"label": "Railing posts spaced to clear parapet deflection joints as per STD-BR-2-15."},
    {"label": "Radius of curved railing not less than 20 feet without special details. This is noted in STD-BR-2-15 "
              "Sheet 5 of 5 Under Horizontal Curvatures Title."},
    {"label": "All horizontal reinforcing steel should be detailed as per STD-BR-2-15."},
    {"label": "Steel tubing has provision for Expansion and Contraction as shown on STD-BR-2-15 Sheet 1 of 5 View D-D."}
]

parapet_railing_criteria = [
    {"label": "Parapet when to use per", "reference": "309.4.3"},
    {"label": "Complete details of the Parapet Type bridge railing shown on the plans?"},
    {"label": "Railing transition preferably mounted on turn back abutment wingwalls or approach slabs?"},
    {"label": "For bridges with expansion joints and with parapets mounted on approach slabs, the 1'-1\" high base "
              "portion of the parapets within the width of back walls are reinforced and placed as part of the "
              "abutments to provide an integral structure for mounting the expansion joint armor?"},
    {"label": "Such parapets provided with special reinforcement and joint details to allow consolidation induced "
              "rotation of the approach slabs without parapet distress?"},
    {"label": "Curb heights on approach slabs limited to 4 inches as shown in Section F-F on Deflector Parapet Type "
              "drawing?"},
    {"label": "Details of filler between approach slab and turn back wing-wall at the base of the parapet made to "
              "conform to DETAIL F of Standard Drawing AS-1-15."},
    {"label": "Parapet length of 14'-0\" or more provided to allow the standard transition length to be used?"},
    {"label": "Reference made to the roadway plans for details and payment provisions for Bridge Terminal Assembly",
     "reference": "Drawings MGS-3.1 and MGS-3.2"}
]

parapet_and_fence_criteria = [
    {"label": "2'-8\" high parapets provided?"},
    {"label": "New guideline for fencing? Fence used on all structure over live traffic except over County and Township"
              " roads."},
    {"label": "Fence details conform to Standard Drawings VPF-1-90?"}
]

elastomeric_bearings_criteria = [
    {"label": "Steel load plate provided for attachment to steel members?", "reference": "306.4.2"},
    {"label": "Elastomer hardness specified?", "reference": "306.4.2"},
    {"label": "An elastomeric pad thickness of 1 inch or more provided (Such pads generally must be reinforced with "
              "steel laminates)?", "reference": "306.4.2"},
    {"label": "A tabulation of unfactored dead load, live load excluding impact, and 'Maximum Design Load' given?"},
    {"label": "For prestressed box beam bridges without external steel load plates, bearing shall conform to Standard "
              "Drawing BD-1-11?"},
    {"label": "Elastomeric bearing with a load plate shall have the plate beveled if the rotation and/or grade exceed "
              "the limitations of AASHTO LRFD 14.7.5.3.3 Method B and 14.7.6.3.5 Method A?"},
    {"label": "Provided with bearing details.", "reference": "Note no. 702.13"},
    {"label": "Top and bottom cover layers should not be thicker than 70% of internal layers",
     "reference": "AASHTO LRFD 14.7.6.1"},
    {"label": "No top cover layer for bearing with load plate.", "reference": "AASHTO LRFD 14.7.6.1"},
    {"label": "Following note included: 'All bearings shall be marked prior to shipping. The marks shall include the "
              "bearing location on the bridge, and a direction arrow that points up-station. All marks shall be "
              "permanent and be visible after the bearing is installed.'"},
    {"label": "A plate bigger than bottom flange on top of HP section so that it can be welded from the top."}
]

anchor_bars_criteria = [
    {"label": "Furnishing and placing anchor bars and ¾” galvanized threaded rod included with Bearing box beams or "
              "I-beams) for payment?", "reference": "Standard Drawing BD-1-11, PSBD-2-07. Not required for PSBD-2-07"},
    {"label": "For steel bearings, furnishing and placing anchor bars included with bearings for payment?",
     "reference": "RB-1-55 and FB-1-82"}
]

anchor_bolt_criteria = [
    {"label": "Outline of masonry plate?"},
    {"label": "Anchor bolt size and embedment length."},
    {"label": "Bearing Anchor Plan to adequately show the location of the bearing anchors with respect to the main "
              "reinforcing bars and the edges of the bridge seats shall be provided.", "reference": "306.2.1.2"}
]

bearings_misc_criteria = [
    {"label": "Movement Provisions: Bearing movement provisions (Fixed, expansion restrained) indicated on the Site "
              "Plan and General Plan?", "reference": "201.1.2.2KI"},
    {"label": "Bearing designation (i.e., R-200) for each substructure unit indicated on the framing plan, beam "
              "elevation, or deck plan?"},
    {"label": "Bearing details or reference to standard drawings given? Separate pay item provided for other than "
              "standard steel bearings (steel bearings for steel bridge are usually included with structural steel for "
              "payment)?"},
    {"label": "Bearing types provided consistent with superstructure movement (longitudinal, lateral, and "
              "rotational)?"},
    {"label": "Bearings/Joints: For bridges with sidewalk, bearing types compatible with deck joint characteristics?"},
    {"label": "Bridge Seats: Bridge seats large enough for the size bearing used taken into account the need for edge "
              "clearances and construction tolerances (wider seats are usually provided for some bridges which are "
              "skewed greater than 30 degrees)?"},
    {"label": "Grade Considerations: Tapered sole plates provided for rocker and bolster bearings for grades of 2 "
              "percent or greater?"},
    {"label": "Coatings: Are notes provided to specify the type of coating required, if other than bare ASTM steel or "
              "Elastomeric bearings?"},
    {"label": "Bridge seats adequate for earthquake provision?", "reference": "306.2.1.1"},
    {"label": "Are seismic restraints required?", "reference": "1003 - S3.10.9.2, 303.1.4.1.a"}
]

deck_joint_terminal_criteria = [
    {"label": "To confine deck drainage, recessed joint seals, joints terminated as shown in Sections A-A and F-F of "
              "Standard Drawings EXJ-2-81 and EXJ-3-82; and Sections B-B and F-F Of Standard Drawing EXJ-4-87 and "
              "EXJ-5-93."},
    {"label": "For new bridges with over the side drainage and wall-type abutments, abutment wing-walls or retaining "
              "walls positioned flush with the back wall to allow extension of sealed deck joints beyond the bridge "
              "seats?"}
]

joint_bearing_coordination_criteria = [
    {"label": "For bridges with elastomeric bearings and sliding plate type joints, bridging plates positioned "
              "cantilevered from the abutment side of the joint to prevent the plate from binding due to the "
              "compressive deflection of the bearings?"},
    {"label": "For sliding plate type joints on grades, a bevel fill attached to the underside of the cantilever plate "
              "to provide a level sliding surface to parallel the direction of bearing movement?"},
    {"label": "Sliding plate type joints avoided on all structures?"}
]

deck_joints_misc_criteria = [
    {"label": "Box Beams: The use of joints generally follows the guidelines given in", "reference": "309.6.3"},
    {"label": "Recessed Seals: Joint seals recessed below the roadway surface (i.e. strip and compression), with "
              "channel deck drainage laterally, detailed to prevent discharge of deck drainage on bridge seats?"},
    {"label": "Adjustment: A joint width adjustment table, in 10 degree increments for 30 degrees to 90 degrees, given "
              "for setting joint widths other than the 60 degree installation temperature? The effect of joint skew "
              "taken into account when computing joint adjustment dimensions?"},
    {"label": "Sawing and Sealing Bituminous Joints detail sheet provided for box beam bridges with poured seal type "
              "joints at abutments?"},
    {"label": "Prestressed concrete I-beam bridges follow the guidelines given in section", "reference": "309.6.3"}
]

scuppers_criteria = [
    {"label": "Is/was the use of scuppers avoided? Scuppers avoided over embankment slopes? Scuppers spaced to clear "
              "cross frames, placed at least 6 feet from the face of piers and abutments; extended at least 8 inches "
              "below beams and girders; located inside of fascia beams of grade separation structures and other highly "
              "visible structures; not been placed through box beams unless such placement cannot be avoided? See BDM "
              "309.7 and 'Bridge Deck Drainage Guidelines,' FHWA HEC 21 & 22."}
]

approach_drainage_criteria = [
    {"label": "Use made of parapet transitions and curbs on approach slabs to channel deck drainage away from "
              "structures towards approach inlets or embankment side slope flumes. See Standard Construction Drawing "
              "DM-4.1."}
]

drainage_collection_criteria = [
    {"label": "These avoided? Where their use cannot be avoided, steepest possible slopes provided? Large sizes used to"
              " help avoid blockage? Convenient clean out provided? Type of field splices specified? Supports adequate "
              "to provide a rigid system?"}
]

elastomeric_trough_criteria = [
    {"label": "Reinforced elastomer required by performance specification?"},
    {"label": "Joint made by vulcanization under heat and pressure?"},
    {"label": "Steep slopes (2 inches per foot or more) used to increase drainage velocity?"},
    {"label": "Large discharge openings (12 inch diameter minimum)?"},
    {"label": "Fasteners for scuppers located outside of the trough for convenient access?"},
    {"label": "Galvanized hardware used?"},
    {"label": "Interior steel surfaces metalized and asphalt coated?"}
]

erosion_protection_criteria = [
    {"label": "Ground surfaces below scuppers protected by crushed aggregate or concrete slope protection?"},
    {"label": "Crushed aggregate or concrete slope protection extended (3'-0\" minimum) beyond edges of open decks?"},
    {"label": "At acute corners of bridges, slope protection extends normal to toe of slope?"}
]

utilities_criteria = [
    {"label": "Documentation on file approved placement of utility on bridge?"},
    {"label": "Concrete embedded utility conduits shown to clear construction joints by 1 inch minimum and other "
              "conduits by 2 inches minimum?"},
    {"label": "Utilities not supported on fascia or below bottom of superstructure? On grade separation structures, no "
              "utilities in bay adjacent to fascia stringer?"},
    {"label": "Gas and water lines not embedded in concrete? Not embedded in section of deck supporting vehicular "
              "traffic?"},
    {"label": "Expansion provisions for utilities shown if appropriate? (Sometimes shown only on utility sheets)"},
    {"label": "Payment for utility supports clearly described by plan note and estimated quantities? (e.g., quantity "
              "table footnote stating portion of Item 513 Structural Steel to be paid for by the utility company)"}
]

grounding_criteria = [
    {"label": "Verify the structure is properly grounded as per Standard Drawing HL-50.21."}
]

approach_slab_criteria = [
    {"label": "Removal of existing approach slab included in the estimated quantities 310.2"},
    {"label": "Removal of existing Wearing Surface included in the estimated quantities as per CMS 202"},
    {"label": "Non-standard approach slab shown 'Modified' in the structure block."},
    {"label": "Current Standard Drawing reference in proposed structure data block and in the General Notes."},
    {"label": "Bars D801 or D802 included in the reinforcing steel list?"},
    {"label": "Pay-Item 526 for Type _ Installation included?"},
    {"label": "Pay-Item for Polymer Modified Asphalt Expansion Joint System or Item 516 – Armorless Preformed Joint "
              "Seal included?"}
]

piers_general_criteria = [
    {"label": "For freestanding piers, is the footing width at least one-fourth the height where founded on soil, "
              "one-fifth the height where founded on rock, and one-fifth the height between centers of outside piles? "
              "306.3.1"},
    {"label": "For cap and column piers on piles or bedrock, columns should generally have separate footings. "
              "306.3.3.1.a"},
    {"label": "Pier cap terminate inside the fascia and drip groove? (For box beam bridges, pier width should allow for"
              " 1/4 inch per joint fit-up between box beams) 308.2.3.3"},
    {"label": "Bearing Anchor Plan shown? Are anchor bolt dimensions normal and parallel to the centerline of "
              "bearing?"},
    {"label": "Cap and column piers preferably designed with a cantilevered cap? 306.3.1"},
    {"label": "For slab bridges, is a construction joint placed at the top of the pier cap? 306.3.3.2"},
    { "label": "Piers in navigable waterways designed to resist collision forces based on AASHTO LRFD bridge design "
               "Specification. 306.3.7"},
    {"label": "Ends of pier caps (all surfaces) under the edge of decks with over-the-side drainage sealed? 306.1.2"},
    {"label": "Appropriate surfaces of roadway shoulder piers sealed? 306.1.2"},
    {"label": "For phased construction, is each phase supported by a minimum of three piles or two drilled shafts? "
              "306.3.1"}
]

pier_pile_criteria = [
    {"label": "Design strives to utilize maximum allowable pile spaces and maximum allowable design loads to minimize "
              "the number of piles 305.3.5.1"},
    {"label": "At least four piles per footing? 305.3.5.1 & 306.3.3.1.a"},
    {"label": "Battered piles required 305.3.5.8"},
    {"label": "Pile spacing a minimum of 2'-6\" or 2.5 times the pile width/diameter? AASHTO LRFD 10.7.1.2"},
    {"label": "Distance from center of piles to edge of footing at least 1'-6\"? 305.3.5.1"},
    {"label": "Can piles be driven without interfering with sheeting, cofferdams, or other bridge or adjacent building "
              "components?"},
    {"label": "Station of intersection of the centerline of bearings and station line."},
    {"label": "Tie the pile spacing to the intersection of the centerline of bearings and station line."},
    {"label": "Number all piles 305.4.4"}
]

capped_pile_piers_criteria = [
    {"label": "Pile spacing less than or equal to 7.5 feet? 305.3.5.1"},
    {"label": "Height above flow line generally limited to 20 feet, or piles specially designed? 306.3.3"},
    {"label": "Distance from edge of pile to face of pier cap is at least 9 inches? 305.3.5.1"},
    {"label": "Pile encasements specified and paid for H-piles)? 606.5-1"},
    {"label": "Minimum of 1'-6\" cover provided above the piles? 305.3.5.1"}
]

cap_and_column_piers_criteria = [
    {"label": "Diameter of the pier column specified to be 3'-0\" and the drilled shaft diameter a minimum of 3'-6\"? "
              "305.4.4.2"},
    {"label": "Location of the construction joint at the pier column/drilled shaft interface appropriate? (Usually 1 "
              "foot above OHWM elevation, for piers in water, and 1 foot below the ground line elsewhere.) 305.4.4"},
    {"label": "A construction joint between the top of drilled shaft and the bottom of the column shown and splice cage"
              " provided? FIG. 303.5.4"},
    {"label": "Reinforcing details at the column/drilled shaft construction joint appropriate? Typically, the "
              "reinforcing cage diameter is a common size between the column, drilled shaft, and bedrock socket."},
    {"label": "Bedrock socket depth shown on the plans? (Bottom of socket elevation should generally not be given) "
              "305.4.2"},
    {"label": "Reinforcing Steel in the drilled shafts? BDM305.4.4.3"},
    {"label": "Spacing of the drilled shafts appropriate? Typically, spacings from 12 to 18 feet are used."},
    {"label": "Drilled shafts should be spaced to utilize the maximum bedrock end bearing pressures and a minimum "
              "number of drilled shafts."}
]

abutments_general_criteria = [
    {"label": "Abutments easily located? Station and overall dimensions?"},
    {"label": "Dimensions referenced from the proper working points? Beam/girder bridges (steel or concrete) "
              "intersection of centerline of survey and centerline of bearings. Concrete slab bridges centerline of "
              "survey is assumed 12 inches behind the face of the abutment. 201.2.1.1"},
    {"label": "Types of Abutments 306.2 & 306.2.2"},
    {"label": "Wing-wall lengths checked?"},
    {"label": "If ground lines are shown, are they appropriate?"},
    {"label": "Earth benches not been used for new designs? Depth of approach slab seat Shown? 306.2.1.4 for CPA-1-08 "
              "abutments"},
    {"label": "Bridge seat sloped to drain toward the face of abutment for beam or girder bridges on spill-through "
              "abutments except at bearings)? (For grade separations on wall-type abutments, are the bridge seats "
              "sloped to drain toward the back wall, with a depressed gutter and drainage system provided? 306.2.3.2"},
    {"label": "For box beam bridges, are provisions necessary to ensure proper fit of the elastomeric bearings i.e., "
              "sloped bridge seats or tapered bearings)? DB-1-11"},
    {"label": "For box beam bridges, is the bridge seat length adequate to support all bearings, accounting for "
              "1/2-inch fit-up per beam joint? Beam seat should not protrude from beneath deck edge when a fit-up "
              "allowance of 1/4 inch per foot is used for pier. 308.2.3.3"},
    {"label": "For box beam bridges, has the proper wearing surface thickness at the abutments being used to compute "
              "bridge seat elevations? 309.1"},
    {"label": "Dowel holes drilled parallel to a free edge clear concrete surface by at least 4 inches?"},
    {"label": "Bearing anchor plan shown? Anchor bolt location dimensions normal and parallel to centerline of bearing?"
              " 306.2.1.2 & 701.2"},
    {"label": "Joint filler shown between concrete box beams and wing-wall concrete? 308.2.3.3"},
    {"label": "Construction joint shown at the level of the approach slab seat for steel superstructures?"},
    {"label": "Construction joint provided in wing-walls of box beam bridges at bridge seat elevation? 308.2.3.3"},
    {"label": "Plan note restricting placement of wing-wall concrete included for box beam bridges?"},
    {"label": "Appropriate surfaces sealed using an appropriate sealer? 306.1.2 & 309.2.1"},
    {"label": "Type 2 waterproofing used at construction joints? Typically used above ground at stage construction "
              "joints, or joints between existing and proposed concrete) 306.2.1.3"},
    {"label": "Expansion & Contraction joints provided as appropriate? 306.2.5"},
    {"label": "Weep-holes located 6 inches to 1 foot above ground level or normal waterline? 306.2.3.3"},
    {"label": "Porous backfill shown 6 inches below weep holes 306.2.3.3"},
    {"label": "Geotextile fabric specified between the porous backfill and the approach fill? Has it been turned up 6 "
              "inches at the wall? 306.2.3.1"},
    {"label": "Lateral limits of porous backfill 2'-0\" thick) clearly indicated in the elevation view as described by "
              "306.2.3.1"},
    {"label": "End caps shown on drain pipes, except at outlets? 306.2.3.1"},
    {"label": "For wall-type abutments where strut action of the superstructure is relied upon for stability, has a "
              "plan note been provided limiting height of backfill until superstructure is placed?"},
    {"label": "Pipe drainage system used? 306.2.3.1"},
    {"label": "For rehabilitation, does the connection between the new and existing concrete appear adequate? Existing "
              "reinforcing that is incorporated into the new work should generally be shown in the proposed "
              "cross-section."},
    {"label": "Aesthetic for wall-type abutments 306.2.2.1"},
    {"label": "For phase construction, is each phase supported by a minimum of three piles or two drilled shafts? "
              "306.2.2.3, 306.2.2.4 & 306.2.2.5"},
    {"label": "Top strap of the MSE wall should be 6” below the footing. See figure 201-2 & 201-3 of the BDM."},
    {"label": "What type of protection is used to prevent the weed growth in the area between the footing and MSE "
              "wall?"},
    {"label": "For high skew semi-integral bridges keep the beam seat level and use variable height of the HP section. "
              "Not possible to bend # 8 bars."}
]

abutment_pile_criteria = [
    {"label": "Flanges of piles parallel to face of rigid abutments; webs parallel to face of flexible abutment "
              "(including CPA-1-08/ICD-1-82 abutments and CPP-1-08 piers)?"},
    {"label": "Battered piles required? (Rate of batter shown? 1:4 desirable, 1:3 acceptable) 305.3.5.8"},
    {"label": "Pile embedment into footing shown as 1'-6\" cover shown above piles or as per 305.3.5"},
    {"label": "Pile design load 305.3.3 & 305.3.4"},
    {"label": "Distance from center of piles to edge of footing at least 1'-6\"? (Not the Ultimate Bearing Value UBV "
              "pile load) shown in the General Notes? UBV as per 305.3.5.1"},
    {"label": "For abutments on a single row of piles, have closed ties been provided around the piles? For example, "
              "see Standard Drawing ICD-1-82"},
    {"label": "Design utilizes maximum allowable pile spacing and maximum allowable design loads to minimize the number"
              " of piles 305.3.5, 305.3.3 & 305.3.4"},
    {"label": "For abutments on a single row of piles, has the footing been extended to the ends of the wingwalls and "
              "straight wing-walls used?"}
]

drilled_shaft_criteria = [
    {"label": "Drilled shaft diameter a minimum of 3'-0\"? 305.4"},
    {"label": "Bedrock socket depth shown on the plans? (Bottom of socket elevation should generally not be given)"},
    {"label": "Spacing of the drilled shafts appropriate? Typically, spacing for 12 to 18 feet are used. Drilled shafts"
              " should attempt to be spaced to utilize the maximum bedrock end bearing pressures and a minimum number "
              "of drilled shafts."},
    {"label": "Splice cage specified? 303.4.4.3 & Fig. 305-4"},
    {"label": "Use of friction drilled shaft requires previous approval of OGE? 305.4.3"}
]

ai_generated = {
    '301':
[
    {
        "label": "Confirm that the disposition of comments from the previous submission (typically Stage 1) is included in the review package.",
        "reference": "BDM 201.4 & L&D Vol 3 1406.4.3"
    },
    {
        "label": "Verify that the Site Plan is included and complies with all Stage 1 review comments.",
        "reference": "BDM 201.4.A & L&D Vol 3 1406.4.3"
    },
    {
        "label": "Verify that a General Plan is included if required for the project.",
        "reference": "BDM 201.4.A & L&D Vol 3 1406.4.3"
    },
    {
        "label": "Verify that General Notes are included in the plan set.",
        "reference": "BDM 201.4.A & L&D Vol 3 1406.4.3"
    },
    {
        "label": "Verify that Estimated Quantities are included, showing all pay items and item extensions (note that quantity values are not required at this stage).",
        "reference": "BDM 201.4.A & L&D Vol 3 1406.4.3"
    },
    {
        "label": "If applicable, verify that Retaining Wall Plans are included and a complete design for each retaining wall is provided in accordance with BDM Section 307.",
        "reference": "BDM 201.4.B, 201.4.1 & 307"
    },
    {
        "label": "If applicable, verify that Noise Barrier Plans are included in accordance with BDM Section 800.",
        "reference": "BDM 201.4.C & 800"
    },
    {
        "label": "Verify that Special Provisions are included in the submission.",
        "reference": "BDM 201.4.D & L&D Vol 3 1406.4.3"
    },
    {
        "label": "Verify that Load Rating Reports for qualifying bridges are submitted.",
        "reference": "BDM 201.4.E, 900, 925.3.3.1, 925.3.3.3, 926.2.2.1, 926.2.2.3 & L&D Vol 3 1406.4.3"
    },
    {
        "label": "Verify that a signed Office of Structural Engineering Bridge Stage 2 Plan Review Checklist is included.",
        "reference": "BDM 201.4.F"
    },
    {
        "label": "Verify that the bridge design conforms to the latest edition of the AASHTO LRFD Bridge Design Specifications.",
        "reference": "BDM 301"
    },
    {
        "label": "Verify that the bridge design conforms to ODOT's supplement to the AASHTO LRFD specifications as documented in BDM Section 1000.",
        "reference": "BDM 301 & 1000"
    },
    {
        "label": "Verify that the design loading includes HL-93 vehicular live load.",
        "reference": "BDM 101.2, 303.1 & 602.2"
    },
    {
        "label": "Verify that the minimum concrete cover for concrete reinforcement meets the requirements of BDM Section 304.4.9 and BDM Section 1005.13.",
        "reference": "BDM 304.4.9 & 1005.13"
    },
    {
        "label": "Verify that minimum concrete reinforcement requirements are met.",
        "reference": "BDM 304.4.10"
    },
    {
        "label": "Verify that foundation analysis for settlement is included and remediation methods are considered if necessary.",
        "reference": "BDM 305.1.3"
    },
    {
        "label": "Verify that all foundation requirements are satisfied for the changes in conditions resulting from the scour design flood (Strength and Service limit states) and the scour check flood (Extreme Event limit states).",
        "reference": "BDM 305.1.6"
    },
    {
        "label": "For new bridges, verify that the design dead load includes an allowance for future wearing surface equal to 0.06-ksf.",
        "reference": "BDM 309.3.2, Figure 309-3 Notes & 602.2"
    },
    {
        "label": "Verify that the transverse deck section includes required information such as deck thickness, crown location, cross slope, railing type, construction joints, out-to-out dimension, face/face railing dimension, reinforcing labels, reinforcing cover, and reinforcing lap location and type.",
        "reference": "BDM 309.3.6"
    },
    {
        "label": "If the bridge crown changes across the structure, verify that a superelevation transition table or diagram (or reference to one) is provided in the plans.",
        "reference": "BDM 201.2.1.1.c, 309.3.6, 309.3.6.1.a & L&D Vol 3 1406.4.3"
    },
    {
        "label": "Verify that bridge railing, transitions, roadway railing, and railing end terminals meet MASH acceptance criteria (TL-3 or TL-5 as required based on route and design speed).",
        "reference": "BDM 309.4.1, 1013.1 & 1013.2"
    },
    {
        "label": "If non-standard railing systems are used, verify that the required submission information (Final Structure Site Plan, Transverse Section, Plan/Elevation/Cross-sections of the railing/transition/roadway railing/end terminal, Traffic data/Design Speed, Cost comparison) was provided to the Office of Structural Engineering for review and acceptance.",
        "reference": "BDM 309.4.1"
    },
    {
        "label": "Verify that plans for concrete bridge railing include provisions to collect and carry deck drainage off the ends of the bridge.",
        "reference": "BDM 309.4.3.1, 309.4.3.2 & 309.4.3.8"
    },
    {
        "label": "Verify that provisions for approach slabs are included for all ODOT bridges.",
        "reference": "BDM 310.2"
    },
    {
        "label": "If standard approach slabs (AS-1-15) are specified, verify that plans include all requirements listed in BDM Section 310.2.1.1.",
        "reference": "BDM 310.2.1.1"
    },
    {
        "label": "Verify that utilities on the bridge (if any) are installed in substantial ducts or enclosures adequate to protect the lines from future bridge repair and maintenance operations.",
        "reference": "BDM 310.4"
    },
    {
        "label": "Verify that plans have been prepared for the Constructability Review.",
        "reference": "L&D Vol 3 1406.4.2"
    },
    {
        "label": "Verify that the construction cost estimate has been updated.",
        "reference": "L&D Vol 3 1406.4.2"
    },
    {
        "label": "Verify that approval from the Design Aesthetics Committee has been obtained for all aesthetic items (e.g., concrete textures, landscape design, color).",
        "reference": "L&D Vol 3 1406.4.2"
    },
    {
        "label": "Verify that the final Post Construction Storm Water Best Management Practices (BMP) design calculations and documentation of any BMP implementation issues are included.",
        "reference": "L&D Vol 2 1112.2 & L&D Vol 3 1406.2.3"
    }
]
}

all_criteria = {
    var_name: globals()[var_name]
    for var_name in globals().keys()
    if var_name.endswith("_criteria") and var_name != "all_comments"  # Exclude itself
}
