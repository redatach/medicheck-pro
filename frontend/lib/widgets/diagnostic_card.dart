import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class DiagnosticCard extends StatelessWidget {
  final String title;
  final String description;
  final String urgency;
  final String recommendations;
  final VoidCallback? onTap;
  
  const DiagnosticCard({
    super.key,
    required this.title,
    required this.description,
    required this.urgency,
    required this.recommendations,
    this.onTap,
  });
  
  Color _getUrgencyColor() {
    switch (urgency.toLowerCase()) {
      case 'emergency':
        return Colors.red;
      case 'high':
        return Colors.orange;
      case 'medium':
        return Colors.yellow.shade700;
      case 'low':
        return Colors.green;
      default:
        return Colors.grey;
    }
  }
  
  String _getUrgencyText() {
    switch (urgency.toLowerCase()) {
      case 'emergency':
        return '🔴 URGENCE';
      case 'high':
        return '🟠 Élevée';
      case 'medium':
        return '🟡 Moyenne';
      case 'low':
        return '🟢 Faible';
      default:
        return urgency;
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 3,
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Text(
                      title,
                      style: GoogleFonts.inter(
                        fontSize: 18,
                        fontWeight: FontWeight.w600,
                        color: Colors.blue.shade900,
                      ),
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      color: _getUrgencyColor().withOpacity(0.1),
                      borderRadius: BorderRadius.circular(20),
                      border: Border.all(
                        color: _getUrgencyColor(),
                        width: 1,
                      ),
                    ),
                    child: Text(
                      _getUrgencyText(),
                      style: GoogleFonts.inter(
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                        color: _getUrgencyColor(),
                      ),
                    ),
                  ),
                ],
              ),
              
              const SizedBox(height: 12),
              
              Text(
                description,
                style: GoogleFonts.inter(
                  fontSize: 14,
                  color: Colors.grey.shade700,
                  height: 1.5,
                ),
                maxLines: 3,
                overflow: TextOverflow.ellipsis,
              ),
              
              const SizedBox(height: 16),
              
              Text(
                '💡 Recommandations:',
                style: GoogleFonts.inter(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                  color: Colors.blue.shade800,
                ),
              ),
              
              const SizedBox(height: 8),
              
              Text(
                recommendations,
                style: GoogleFonts.inter(
                  fontSize: 13,
                  color: Colors.grey.shade800,
                  height: 1.5,
                ),
                maxLines: 3,
                overflow: TextOverflow.ellipsis,
              ),
              
              const SizedBox(height: 16),
              
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Voir les détails →',
                    style: GoogleFonts.inter(
                      fontSize: 14,
                      color: Colors.blue.shade600,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  const Icon(
                    Icons.arrow_forward_ios,
                    size: 16,
                    color: Colors.blue,
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
